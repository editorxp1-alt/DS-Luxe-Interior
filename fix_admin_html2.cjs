const fs = require("fs"); 
let content = fs.readFileSync("admin.html", "utf8"); 

content = content.replace(/Image upload ke liye ImgBB[\s\S]*?id="save-key-btn" class="key-save-btn">Save Key<\/button>\s*<\/div>/, `Uploads are now saved directly to the local server storage. API Key is no longer required.
            </p>
            <div class="key-input-row" style="display:none;">
              <input type="text" id="imgbb-key" />
              <button id="save-key-btn" class="key-save-btn">Save Key</button>
            </div>`);

fs.writeFileSync("admin.html", content);
