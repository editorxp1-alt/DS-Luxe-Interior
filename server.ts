import express from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { createServer as createViteServer } from 'vite';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';

const app = express();
const PORT = 3000;

app.use(express.json());

// Initialize Firebase
const firebaseConfig = JSON.parse(fs.readFileSync('./firebase-applet-config.json', 'utf-8'));
const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp, firebaseConfig.firestoreDatabaseId);

// In-memory data store for the gallery (replacing JSONBin)
let galleryData: any[] = [];
let reviewsData: any[] = [];

async function syncData() {
  try {
    const gallerySnap = await getDoc(doc(db, 'data', 'gallery'));
    if (gallerySnap.exists()) {
      galleryData = gallerySnap.data().record || [];
    } else {
      const dataPath = path.resolve('./gallery-data.json');
      if (fs.existsSync(dataPath)) {
        galleryData = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
        await setDoc(doc(db, 'data', 'gallery'), { record: galleryData });
      }
    }

    const reviewsSnap = await getDoc(doc(db, 'data', 'reviews'));
    if (reviewsSnap.exists()) {
      reviewsData = reviewsSnap.data().record || [];
    } else {
      const reviewsPath = path.resolve('./reviews.json');
      if (fs.existsSync(reviewsPath)) {
        reviewsData = JSON.parse(fs.readFileSync(reviewsPath, 'utf-8'));
        await setDoc(doc(db, 'data', 'reviews'), { record: reviewsData });
      }
    }
    console.log("Firebase synced successfully.");
  } catch (error) {
    console.error("Error syncing with Firebase:", error);
  }
}

// Call sync immediately to load data from Firebase on startup
syncData();

const uploadsDir = path.resolve('./public/uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Ensure public directory is accessible
app.use(express.static(path.resolve('./public')));

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadsDir)
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
    cb(null, uniqueSuffix + '-' + file.originalname)
  }
})
const upload = multer({ storage: storage })

app.get('/api/reviews', (req, res) => {
  res.json({ record: reviewsData });
});

app.post('/api/reviews', async (req, res) => {
  const newReview = req.body;
  newReview.timestamp = Date.now();
  reviewsData.unshift(newReview);
  
  try {
    await setDoc(doc(db, 'data', 'reviews'), { record: reviewsData });
    res.json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, error: "Failed to save to database" });
  }
});

app.get('/api/gallery', (req, res) => {
  res.json({ record: galleryData });
});

app.put('/api/gallery', async (req, res) => {
  galleryData = req.body;
  
  try {
    await setDoc(doc(db, 'data', 'gallery'), { record: galleryData });
    res.json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, error: "Failed to save to database" });
  }
});

app.post('/api/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: { message: 'No file uploaded' } });
  }
  const url = `/uploads/${req.file.filename}`;
  res.json({ success: true, data: { url: url } });
});

async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa'
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.resolve('./dist')));
    app.get('*', (req, res) => {
      res.sendFile(path.resolve('./dist/index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
