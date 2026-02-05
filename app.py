import re
import requests
from flask import Flask, request, jsonify, render_template_string
from bs4 import BeautifulSoup
from humanize import naturalsize
from urllib.parse import quote, unquote
import os

app = Flask(__name__)

cookies = {"ndus": "YbDgQCEteHui0Bx8sPAmBS3hSB4K79edBrj6PrJq"}
json_data_url = "https://www.4funbox.com/share/list?jsToken={jsToken}&shorturl={key}"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>TeraBox Bypass</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        p {
            color: #666;
            margin-bottom: 30px;
        }
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        #result {
            margin-top: 30px;
        }
        .file-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        .file-item h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .file-item p {
            color: #666;
            margin-bottom: 5px;
        }
        .download-link {
            display: inline-block;
            margin-top: 10px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .download-link:hover {
            background: #764ba2;
        }
        .error {
            background: #fee;
            border-left-color: #f44;
            color: #c33;
        }
        .loading {
            text-align: center;
            color: #667eea;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 TeraBox Bypass</h1>
        <p>Get direct download links for TeraBox files</p>
        
        <div class="input-group">
            <input type="text" id="url" placeholder="Enter TeraBox URL..." />
            <button onclick="bypass()">Get Links</button>
        </div>
        
        <div id="result"></div>
    </div>

    <script>
        async function bypass() {
            const url = document.getElementById('url').value;
            const resultDiv = document.getElementById('result');
            
            if (!url) {
                resultDiv.innerHTML = '<div class="file-item error"><p>Please enter a URL</p></div>';
                return;
            }
            
            resultDiv.innerHTML = '<div class="loading">Processing... Please wait</div>';
            
            try {
                const response = await fetch('/api/bypass', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    resultDiv.innerHTML = `<div class="file-item error"><p>${data.error}</p></div>`;
                    return;
                }
                
                if (data.files && data.files.length > 0) {
                    resultDiv.innerHTML = data.files.map(file => `
                        <div class="file-item">
                            <h3>📄 ${file.title}</h3>
                            ${file.path ? `<p><strong>Path:</strong> ${file.path}</p>` : ''}
                            <p><strong>Size:</strong> ${file.size}</p>
                            <a href="${file.dlink}" class="download-link" target="_blank">Download</a>
                        </div>
                    `).join('');
                } else {
                    resultDiv.innerHTML = '<div class="file-item error"><p>No files found</p></div>';
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="file-item error"><p>Error: ${error.message}</p></div>`;
            }
        }
        
        document.getElementById('url').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') bypass();
        });
    </script>
</body>
</html>
'''

def process_terabox(terabox_url):
    try:
        req = requests.get(terabox_url, cookies=cookies, timeout=10)
        soup = BeautifulSoup(req.content, "html.parser")
        scripts = soup.find_all("script")
        
        if len(scripts) < 4:
            return None, None
            
        result = scripts[3]
        jsToken = None
        
        if match := re.search(r'"([^"]+)"', unquote(result.text)):
            jsToken = match.group(1)
        
        key = req.url.split("=")[1] if "=" in req.url else None
        
        return jsToken, key
    except Exception as e:
        print(f"Error processing TeraBox URL: {e}")
        return None, None

def bypass_directory_logic(jsToken, key, link, cookies, depth=0):
    files = []
    if depth >= 10:
        return files
    
    try:
        res = requests.get(link, cookies=cookies, timeout=10)
        data = res.json()
        
        if "list" in data:
            for item in data["list"]:
                if "dlink" in item:
                    path = item['path'].rsplit("/", 1)
                    files.append({
                        "path": path[0] if len(path) > 1 else "",
                        "title": item['server_filename'],
                        "size": naturalsize(item['size']),
                        "dlink": item['dlink']
                    })
                
                if "path" in item and "dlink" not in item:
                    _path = quote(item["path"]).replace("/", "%2F")
                    sub_link = f"{json_data_url.format(jsToken=jsToken, key=key)}&dir={_path}"
                    files.extend(bypass_directory_logic(jsToken, key, sub_link, cookies, depth + 1))
    except Exception as e:
        print(f"Error in bypass_directory_logic: {e}")
    
    return files

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/bypass', methods=['POST'])
def api_bypass():
    try:
        data = request.json
        terabox_url = data.get('url', '')
        
        if not terabox_url:
            return jsonify({"error": "URL is required"}), 400
        
        jsToken, key = process_terabox(terabox_url)
        
        if not jsToken or not key:
            return jsonify({"error": "Failed to process TeraBox URL. Please check the URL and try again."}), 400
        
        base = json_data_url.format(jsToken=jsToken, key=key)
        res = requests.get(f"{base}&root=1", cookies=cookies, timeout=10)
        
        files = []
        
        try:
            meta = res.json()["list"][0]
            if "dlink" in meta:
                files.append({
                    "title": meta['server_filename'],
                    "size": naturalsize(meta['size']),
                    "dlink": meta['dlink'],
                    "path": ""
                })
            else:
                _path = quote(meta["path"]).replace("/", "%2F")
                link = f'{json_data_url.format(jsToken=jsToken, key=key)}&dir={_path}'
                files = bypass_directory_logic(jsToken, key, link, cookies)
        except (KeyError, IndexError):
            return jsonify({"error": "Failed to retrieve file information"}), 400
        
        return jsonify({"files": files})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
