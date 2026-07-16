const ADMIN_HASH =  "94b271d20205e6af0e88cb7b7c3cc60d479a283c211cf8379c0d21a3d5816095";

const JSONBIN_ID = '6a5772b4da38895dfe60ab40';
const JSONBIN_KEY = '$2a$10$dySlyKWtDmqIrrOcquURWeinFotbSXwgwZHeC6Bqu9RHcaE5T5KWu';
const GET_URL = `https://api.jsonbin.io/v3/b/${JSONBIN_ID}`;
const PUT_URL = `https://api.jsonbin.io/v3/b/${JSONBIN_ID}`;

// DOM Elements
const loginSection = document.getElementById("login-section");
const panelSection = document.getElementById("panel-section");
const loginMsg = document.getElementById("login-msg");
const saveMsg = document.getElementById("save-msg");
const uploadMsg = document.getElementById("upload-msg");
const serviceSelect = document.getElementById("service-select");
const mediaGrid = document.getElementById("media-grid");
const keyMsg = document.getElementById("key-msg");

let galleryData = [];
let currentSlug = "";

// ─── Utility ────────────────────────────────────────────────
async function hashPassword(pwd) {
  const buf = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(pwd),
  );
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

// ─── Settings ────────────────────────────────
window.toggleSettings = function toggleSettings() {
  const body = document.getElementById("settings-body");
  const arrow = document.getElementById("settings-arrow");
  body.classList.toggle("hidden");
  arrow.classList.toggle("open");
}

document.getElementById("save-key-btn").onclick = () => {
  keyMsg.textContent = "✅ Updated! Uploads now use local server.";
  keyMsg.style.color = "#4ade80";
  setTimeout(() => { keyMsg.textContent = ""; }, 3000);
};

// ─── 1. Login ───────────────────────────────────────────────
document.getElementById("login-btn").onclick = async () => {
  const entered = document.getElementById("admin-pass").value.trim();
  if (!entered) return (loginMsg.textContent = "🔒 Please enter a password.");
  const hash = await hashPassword(entered);
  if (hash !== ADMIN_HASH) return (loginMsg.textContent = "❌ Wrong password.");
  loginSection.classList.add("hidden");
  panelSection.classList.remove("hidden");
  loadData();
};

// ─── 2. Load Data from JSONBin ──────────────────────────────
async function loadData() {
  saveMsg.textContent = "Loading gallery data...";
  try {
    const res = await fetch(GET_URL, {
      headers: {
        'X-Master-Key': JSONBIN_KEY
      }
    });
    const json = await res.json();
    galleryData = json.record || [];
    saveMsg.textContent = "";
    populateDropdown();
  } catch (e) {
    saveMsg.textContent = "❌ Failed to load data.";
  }
}

function populateDropdown() {
  serviceSelect.innerHTML = "";
  galleryData.forEach((s) => {
    const opt = document.createElement("option");
    opt.value = s.slug;
    opt.textContent = s.title;
    serviceSelect.appendChild(opt);
  });
  if (galleryData.length > 0) {
    currentSlug = galleryData[0].slug;
    renderMedia();
  }
}

serviceSelect.onchange = (e) => {
  currentSlug = e.target.value;
  renderMedia();
};

// ─── 3. Render Media Grid ───────────────────────────────────
function renderMedia() {
  mediaGrid.innerHTML = "";
  const service = galleryData.find((s) => s.slug === currentSlug);
  if (!service) return;
  // Render images
  if (service.images) {
    service.images.forEach((url, idx) => {
      mediaGrid.appendChild(
        createMediaCard(url, "image", "📷 Photo", () => {
          service.images.splice(idx, 1);
          renderMedia();
        }),
      );
    });
  }
  // Render youtube
  if (service.youtube) {
    service.youtube.forEach((url, idx) => {
      const vid = ytId(url) || url;
      mediaGrid.appendChild(
        createMediaCard(
          `https://img.youtube.com/vi/${vid}/hqdefault.jpg`,
          "youtube",
          "🎬 YouTube",
          () => {
            service.youtube.splice(idx, 1);
            renderMedia();
          },
        ),
      );
    });
  }
}

function createMediaCard(imgSrc, type, label, onDelete) {
  const div = document.createElement("div");
  div.className = "media-item";
  div.innerHTML = `
    <img src="${imgSrc}" loading="lazy">
    <span class="type-badge">${label}</span>
    <button class="delete-btn" title="Delete">✕</button>
  `;
  div.querySelector(".delete-btn").onclick = onDelete;
  return div;
}

function ytId(url) {
  const m = url.match(
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([^&\n?#]+)/,
  );
  return m ? m[1] : url;
}

// ─── 4. Image Upload (Local Server) ───────────
document.getElementById("image-upload").onchange = async (e) => {
  const files = e.target.files;
  if (!files || files.length === 0) return;
  
  const service = galleryData.find((s) => s.slug === currentSlug);
  if (!service) return;
  if (!service.images) service.images = [];
  
  const progressBar = document.getElementById("upload-progress");
  const progressFill = document.getElementById("progress-fill");
  const uploadBox = document.querySelector(".upload-box");
  uploadBox.classList.add("uploading");
  progressBar.classList.remove("hidden");
  
  const total = files.length;
  let uploaded = 0;
  let failed = 0;
  uploadMsg.textContent = `Uploading 0/${total}...`;
  uploadMsg.style.color = "#60a5fa";
  
  for (const file of files) {
    try {
      const formData = new FormData();
      formData.append("image", file);
      const res = await fetch(`/api/upload`, {
        method: "POST",
        body: formData,
      });
      const json = await res.json();
      if (json.success) {
        service.images.push(json.data.url);
        uploaded++;
      } else {
        failed++;
        const errMsg = json.error ? json.error.message : JSON.stringify(json);
        console.error("Upload error:", errMsg);
        uploadMsg.textContent = `❌ Error: ${errMsg}`;
        uploadMsg.style.color = "#f87171";
      }
    } catch (err) {
      failed++;
      console.error("Upload error:", err);
      uploadMsg.textContent = `❌ Network error: ${err.message}`;
      uploadMsg.style.color = "#f87171";
    }
    const pct = Math.round(((uploaded + failed) / total) * 100);
    progressFill.style.width = pct + "%";
    if (failed === 0)
      uploadMsg.textContent = `Uploading ${uploaded + failed}/${total}...`;
  }
  
  uploadBox.classList.remove("uploading");
  progressFill.style.width = "100%";
  if (failed === 0) {
    uploadMsg.textContent = `✅ ${uploaded} image${uploaded > 1 ? "s" : ""} uploaded! Don't forget to Save.`;
    uploadMsg.style.color = "#4ade80";
  } else if (uploaded > 0) {
    uploadMsg.textContent = `⚠️ ${uploaded} uploaded, ${failed} failed.`;
    uploadMsg.style.color = "#fbbf24";
  }
  setTimeout(() => {
    progressBar.classList.add("hidden");
    progressFill.style.width = "0%";
  }, 2000);
  
  renderMedia();
  e.target.value = "";
};

// ─── 5. Add YouTube Video ───────────────────────────────────
document.getElementById("add-yt-btn").onclick = () => {
  const input = document.getElementById("yt-url");
  const url = input.value.trim();
  if (!url) return;
  const service = galleryData.find((s) => s.slug === currentSlug);
  if (!service.youtube) service.youtube = [];
  service.youtube.push(url);
  input.value = "";
  renderMedia();
};

// ─── 6. Save to JSONBin ─────────────────────────────────────
document.getElementById("save-btn").onclick = async () => {
  saveMsg.textContent = "💾 Saving changes to server...";
  saveMsg.style.color = "#60a5fa";
  try {
    await fetch(PUT_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-Master-Key": JSONBIN_KEY
      },
      body: JSON.stringify(galleryData),
    });
    saveMsg.textContent = "✅ All changes saved!";
    saveMsg.style.color = "#4ade80";
    setTimeout(() => (saveMsg.textContent = ""), 3000);
  } catch (e) {
    saveMsg.textContent = "❌ Save failed: " + e;
    saveMsg.style.color = "#f87171";
  }
};
