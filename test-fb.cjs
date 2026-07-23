const { initializeApp } = require('firebase/app');
const { getFirestore, doc, getDoc, setDoc } = require('firebase/firestore');
const fs = require('fs');

const firebaseConfig = JSON.parse(fs.readFileSync('./firebase-applet-config.json', 'utf-8'));
const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp, firebaseConfig.firestoreDatabaseId);

async function test() {
  try {
    const gallerySnap = await getDoc(doc(db, 'data', 'gallery'));
    console.log('Exists?', gallerySnap.exists());
    if (gallerySnap.exists()) {
       console.log(gallerySnap.data());
    } else {
       console.log('Not exists, writing...');
       await setDoc(doc(db, 'data', 'gallery'), { record: [1, 2, 3] });
       console.log('Written.');
    }
  } catch (e) {
    console.error(e);
  }
}
test();
