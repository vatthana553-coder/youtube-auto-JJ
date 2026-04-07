# Deploy to Hugging Face Spaces

This project can be deployed publicly for free on [Hugging Face Spaces](https://huggingface.co/spaces) using Gradio.

## Quick Deploy Steps

### Option 1: One-Click Deploy (Recommended)

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in:
   - **Space name**: `faceless-viral-video-bot` (or your choice)
   - **License**: MIT
   - **Visibility**: Public
4. Choose **Gradio** as SDK
5. Select **Python** as SDK version
6. Choose hardware: **CPU Basic** (free tier works!)
7. Click "Create Space"

8. After creation, go to your Space → Files → Add file → Create a new file
9. Copy the contents of this repository:
   - `app.py` (main Gradio interface)
   - `src/` folder (all source code)
   - `config.yaml`
   - `requirements.txt`

10. Commit changes and wait for build (~2-5 minutes)
11. Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/faceless-viral-video-bot`

### Option 2: Deploy via Git

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/faceless-viral-video-bot
cd faceless-viral-video-bot

# Copy project files
cp -r /path/to/faceless_viral_video_bot/* .

# Push to Hugging Face
git add .
git commit -m "Initial commit"
git push
```

## Required Files for Hugging Face

Make sure these files are in your Space:

✅ `app.py` - Gradio web interface  
✅ `requirements.txt` - Python dependencies  
✅ `src/` - All source modules  
✅ `config.yaml` - Configuration  
✅ `.gitignore` - Ignore unnecessary files  

## Hardware Requirements

- **Free Tier (CPU Basic)**: Works for script generation, subtitles, visuals
- **Note**: TTS (edge-tts) requires internet connection
- **Video rendering**: May be slow on free tier; consider upgrading for heavy use

## Environment Variables (Optional)

If you want to add optional API integrations:

1. Go to your Space → Settings → Repository secrets
2. Add secrets like:
   - `HF_TOKEN` - For Hugging Face models
   - `OPENAI_API_KEY` - If using OpenAI (optional)

## Accessing Your Public App

Once deployed, anyone can access your app at:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

You can:
- Share the link on social media
- Embed it on websites
- Use the API endpoint (if enabled)

## Troubleshooting

### Build Fails
- Check `requirements.txt` syntax
- Ensure all imports in `app.py` are correct
- Look at build logs in Space → Logs

### Runtime Errors
- Check if all `src/` modules are present
- Verify `config.yaml` is valid YAML
- Ensure FFmpeg is available (pre-installed on HF Spaces)

### Slow Performance
- Video rendering is CPU-intensive
- Consider using "Upgrade" button for better hardware
- Or generate assets separately and download

## Alternative Deployment Options

### 1. Render.com (Free Tier)
```yaml
# render.yaml
services:
  - type: web
    name: faceless-video-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    plan: free
```

### 2. Railway.app
- Connect GitHub repo
- Auto-detects Python
- Deploy with one click

### 3. Google Colab (For Testing)
```python
# In Colab notebook:
!git clone https://github.com/YOUR_USERNAME/faceless_viral_video_bot
%cd faceless_viral_video_bot
!pip install -r requirements.txt
!python app.py --share  # Creates public ngrok tunnel
```

### 4. Local Network (For Demo)
```bash
python app.py --server_name 0.0.0.0 --server_port 7860
# Access from other devices: http://YOUR_IP:7860
```

## Usage Example (Public Demo)

Once deployed, users can:
1. Select niche (facts, history, science, etc.)
2. Choose duration (20-60 seconds)
3. Pick tone (dramatic, curious, etc.)
4. Select voice and subtitle style
5. Click "Generate Video"
6. Download all assets from project folder

## Cost Breakdown

| Platform | Free Tier | Paid Options |
|----------|-----------|--------------|
| Hugging Face | ✅ CPU Basic | $5-20/mo for GPU |
| Render | ✅ 750 hrs/mo | $7/mo+ |
| Railway | ✅ 500 hrs/mo | $5/mo+ |
| Colab | ✅ Limited GPU | $10/mo Pro |

**Recommendation**: Start with Hugging Face Spaces free tier for testing!

## Sharing Your Creation

Once live, share your bot:
- Twitter/X: "Check out my AI YouTube Shorts generator! 🎬"
- Reddit: r/youtube, r/contentcreation, r/automation
- Discord: Creator communities
- TikTok: Make videos ABOUT making videos (meta!)

---

🚀 **Happy Deploying!**

Your faceless video automation system is now accessible to the world!
