const fs = require("fs"); 
let content = fs.readFileSync("admin.js", "utf8"); 

content = content.replace(/async function loadData\(\) \{[\s\S]*?renderMedia\(\);\n  \}\n\}/, `async function loadData() {
  saveMsg.textContent = "Loading gallery data...";
  try {
    const res = await fetch(GET_URL);
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
}`);

fs.writeFileSync("admin.js", content);
