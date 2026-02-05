# TeraBox Bypass - Railway Deployment Guide

## 🚀 Quick Deploy to Railway

### Method 1: GitHub + Railway (Recommended)

1. **Create a GitHub Repository**
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it something like `terabox-bypass`
   - Keep it private if you prefer

2. **Upload Files to GitHub**
   - Upload these files to your repository:
     - `app.py`
     - `requirements.txt`
     - `Procfile`
     - `runtime.txt`
     - `README.md` (optional)

3. **Deploy on Railway**
   - Go to [Railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `terabox-bypass` repository
   - Railway will automatically detect it's a Python app and deploy!

### Method 2: Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and Deploy**
   ```bash
   cd /path/to/your/project
   railway init
   railway up
   ```

## 📁 Files Included

- **app.py** - Main Flask web application with beautiful UI
- **requirements.txt** - Python dependencies
- **Procfile** - Tells Railway how to run your app
- **runtime.txt** - Specifies Python version
- **terabox-bypass.py** - Original CLI script (optional)

## 🎨 Features

Your deployed app includes:
- ✨ Beautiful gradient UI
- 🔗 Paste TeraBox URL and get direct download links
- 📦 Handles both single files and directories
- 💾 Shows file size and path information
- 📱 Responsive design works on mobile

## 🔧 Configuration

The app runs on the port specified by Railway's `PORT` environment variable (automatically configured).

## 📝 How to Use After Deployment

1. Once deployed, Railway will give you a URL like: `https://your-app.railway.app`
2. Open the URL in your browser
3. Paste any TeraBox share URL
4. Click "Get Links" to get direct download links!

## 🐛 Troubleshooting

**App won't start?**
- Check Railway logs for errors
- Make sure all files are uploaded correctly
- Verify `requirements.txt` has all dependencies

**Getting errors when processing URLs?**
- The TeraBox URL might have expired
- Try with a different TeraBox share link
- Check if the API endpoint is still working

## 🔐 Security Note

This app bypasses TeraBox download limits. Use responsibly and only with content you have permission to access.

## 📚 API Endpoint

If you want to use it programmatically:

```bash
curl -X POST https://your-app.railway.app/api/bypass \
  -H "Content-Type: application/json" \
  -d '{"url":"https://teraboxapp.com/s/YOUR_SHARE_LINK"}'
```

## 💡 Tips

- Keep your Railway app private if processing sensitive content
- Railway free tier has usage limits - monitor your usage
- You can add custom domain in Railway settings

## 🎉 That's It!

Your TeraBox bypass tool is now live and accessible from anywhere!
