const { initializeApp } = require('firebase/app');
const { getStorage, ref, uploadBytes, getDownloadURL } = require('firebase/storage');
const fs = require('fs');

const firebaseConfig = JSON.parse(fs.readFileSync('./firebase-applet-config.json', 'utf-8'));
const firebaseApp = initializeApp(firebaseConfig);
const storage = getStorage(firebaseApp);

async function test() {
  try {
    const storageRef = ref(storage, 'test.txt');
    const bytes = new Uint8Array(Buffer.from('Hello world'));
    await uploadBytes(storageRef, bytes);
    const url = await getDownloadURL(storageRef);
    console.log("Success! URL:", url);
  } catch (e) {
    console.error("Storage error:", e);
  }
}
test();
