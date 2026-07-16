const ADMIN_HASH =  "94b271d20205e6af0e88cb7b7c3cc60d479a283c211cf8379c0d21a3d5816095";

const JSONBIN_ID = '6a5772b4da38895dfe60ab40';
const JSONBIN_KEY = '$2a$10$dySlyKWtDmqIrrOcquURWeinFotbSXwgwZHeC6Bqu9RHcaE5T5KWu';
const GET_URL = "https://api.jsonbin.io/v3/b/" + JSONBIN_ID;
const PUT_URL = "https://api.jsonbin.io/v3/b/" + JSONBIN_ID;

// DOM Elements
const loginSection = document.getElementById("login-section");
const panelSection = document.getElementById("panel-section");
const loginMsg = document.getElementById("login-msg");
const saveMsg = document.getElementById("save-msg");
const uploadMsg = document.getElementById("upload-msg");
const serviceSelect = document.getElementById("service-select");
const mediaGrid = document.getElementById("media-grid");

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
          "https://img.youtube.com/vi/" + vid + "/hqdefault.jpg",
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
    <img src="` + imgSrc + `" loading="lazy">
    <span class="type-badge">` + label + `</span>
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

// ─── 4. Image URL Add ───────────
document.getElementById("add-img-btn").onclick = () => {
  const input = document.getElementById("img-url");
  const url = input.value.trim();
  if (!url) return;
  const service = galleryData.find((s) => s.slug === currentSlug);
  if (!service) return;
  if (!service.images) service.images = [];
  service.images.push(url);
  input.value = "";
  renderMedia();
  uploadMsg.textContent = "✅ Image added! Don't forget to Save All Changes.";
  uploadMsg.style.color = "#4ade80";
  setTimeout(() => { uploadMsg.textContent = ""; }, 3000);
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
