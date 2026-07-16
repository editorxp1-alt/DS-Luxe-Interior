const fs = require("fs"); 
let content = fs.readFileSync("gallery.html", "utf8"); 

content = content.replace(/const JSONBIN_ID[\s\S]*?const SVCS =/, "const SVCS =");
content = content.replace(/const res = await fetch\(`https:\/\/api\.jsonbin\.io\/v3\/b\/\$\{JSONBIN_ID\}`[\s\S]*?\}\);/, "const res = await fetch(`/api/gallery`);");

fs.writeFileSync("gallery.html", content);
