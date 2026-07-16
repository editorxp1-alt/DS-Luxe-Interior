import express from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { createServer as createViteServer } from 'vite';

const app = express();
const PORT = 3000;

app.use(express.json());

// In-memory data store for the gallery (replacing JSONBin)
let galleryData = [
  {
    "slug": "kitchen",
    "title": "Modular Kitchen",
    "images": [
      "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1588854337236-6889d631faa8?auto=format&fit=crop&w=1200&q=84"
    ]
  },
  {
    "slug": "wardrobe",
    "title": "Luxury Wardrobes",
    "images": [
      "https://images.unsplash.com/photo-1595514535313-90d1f8876c1f?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1558997519-83ea9252edf8?auto=format&fit=crop&w=1200&q=84"
    ]
  },
  {
    "slug": "living",
    "title": "Living Room Interiors",
    "images": [
      "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=84"
    ]
  },
  {
    "slug": "bedroom",
    "title": "Bedroom Interiors",
    "images": [
      "https://images.unsplash.com/photo-1616137466211-f939a420be84?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=1200&q=84",
      "https://images.unsplash.com/photo-1505693314120-0d443867891c?auto=format&fit=crop&w=1200&q=84"
    ]
  }
];

const dataPath = path.resolve('./gallery-data.json');
if (fs.existsSync(dataPath)) {
  try {
    galleryData = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
  } catch (e) {
    console.error("Failed to parse local gallery data");
  }
}

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

app.get('/api/gallery', (req, res) => {
  res.json({ record: galleryData });
});

app.put('/api/gallery', (req, res) => {
  galleryData = req.body;
  fs.writeFileSync(dataPath, JSON.stringify(galleryData, null, 2));
  res.json({ success: true });
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
