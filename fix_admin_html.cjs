const fs = require("fs"); 
let content = fs.readFileSync("admin.html", "utf8"); 

content = content.replace(/Image upload ke liye ImgBB API key chahiye[\s\S]*?ImgBB\.com<\/a>[\s\S]*?id="imgbb-key"[\s\S]*?Save API Key<\/button>/, "Images are now saved directly to the local server storage. ImgBB API Key is no longer required.\n            </p>\n            <button id=\"save-key-btn\" style=\"margin-top: 10px;\">Acknowledge</button>");

fs.writeFileSync("admin.html", content);
