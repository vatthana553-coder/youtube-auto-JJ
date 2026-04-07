# Faceless Viral Video Bot

A complete AI-powered faceless YouTube automation system inspired by cinematic storytelling channels. This system automatically generates highly engaging, curiosity-driven YouTube Shorts or TikTok-style videos using only free and open-source tools.

## 🎯 Features

- **Topic & Idea Generator**: Generate viral content ideas across multiple niches
- **Script Writer**: Create 20-60 second scripts optimized for retention
- **Voice Generation**: Free TTS with multiple voices (Coqui TTS, Piper, edge-tts)
- **Subtitle Generator**: Word-level/sentence-level captions with styling
- **Visual Generation**: AI-generated or stock footage with motion effects
- **Video Assembler**: Combine all elements into vertical 9:16 videos
- **Metadata Generator**: Titles, descriptions, hashtags, and thumbnail text
- **Workflow Automation**: CLI and web UI options

## 📁 Project Structure

```
faceless_viral_video_bot/
├── src/
│   ├── generators/          # Script, topic, metadata generation
│   ├── processors/          # Audio, subtitle, visual processing
│   ├── assemblers/          # Video assembly and editing
│   └── utils/               # Utilities, config, logging
├── config/                  # Configuration files
├── templates/               # Prompt templates
├── projects/                # Generated projects
│   └── demo_project/
│       ├── script/
│       ├── audio/
│       ├── visuals/
│       ├── subtitles/
│       ├── output/
│       └── metadata/
├── assets/                  # Stock media, music, SFX
├── tests/                   # Test files
├── requirements.txt
├── config.yaml
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- Optional: GPU for faster AI inference

### Installation

1. **Clone the repository** (or navigate to the project folder)

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg**:
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg` or `sudo yum install ffmpeg`

4. **Optional: Install Ollama for local LLM**:
```bash
# Visit https://ollama.ai for installation instructions
ollama pull llama2
```

5. **Optional: Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys (only needed if using optional APIs)
```

## 🎬 Usage

### Command Line Interface

Run the main pipeline:

```bash
python src/main.py --niche "science" --duration 45 --voice "default"
```

Or use the interactive mode:

```bash
python src/main.py --interactive
```

### Web UI (Optional)

Launch the Streamlit interface:

```bash
streamlit run src/web_ui.py
```

### Generate a Demo Video

```bash
python src/main.py --demo
```

This will create a complete demo project in `projects/demo_project/`.

## ⚙️ Configuration

Edit `config.yaml` to customize:

- Default niche and topics
- Voice settings (speed, pitch)
- Visual style preferences
- Output format and resolution
- TTS engine selection
- LLM provider settings

Example configuration:

```yaml
general:
  project_name: "my_viral_short"
  duration: 45
  resolution: "1080x1920"
  fps: 30

niche:
  default: "science"
  available: ["facts", "history", "science", "mysteries", "finance", "what_if"]

tts:
  engine: "edge-tts"  # Options: edge-tts, piper, coqui
  voice: "en-US-JennyNeural"
  speed: 1.0
  pitch: 0

visuals:
  style: "ai_generated"  # Options: ai_generated, stock, mixed
  motion_effects: true
  ken_burns: true

llm:
  provider: "ollama"  # Options: ollama, huggingface, openai (optional)
  model: "llama2"
  max_tokens: 500
```

## 🎭 Available Niches

- **Facts**: Mind-blowing facts and trivia
- **History**: Historical events and figures
- **Science**: Scientific discoveries and concepts
- **Mysteries**: Unsolved mysteries and conspiracies
- **Finance**: Money tips and financial facts
- **What If**: Hypothetical scenarios

## 🔧 Modules Overview

### 1. Topic Generator (`src/generators/topic_generator.py`)
Generates viral content ideas based on selected niche. Saves ideas to JSON/CSV.

### 2. Script Writer (`src/generators/script_writer.py`)
Creates 20-60 second scripts with:
- Strong hooks (first 3 seconds)
- Buildup with pacing
- Surprise payoff/ending
- Timestamped scene instructions

### 3. Voice Generator (`src/processors/voice_processor.py`)
Supports multiple free TTS engines:
- **edge-tts**: Microsoft's free neural TTS
- **Piper**: Fast local TTS
- **Coqui TTS**: Open-source TTS with voice cloning

### 4. Subtitle Generator (`src/processors/subtitle_processor.py`)
Creates styled subtitles with:
- Word-level or sentence-level timing
- Bold text and keyword highlighting
- Dynamic placement and animations

### 5. Visual Generator (`src/processors/visual_processor.py`)
Generates or sources visuals:
- AI image generation (Stable Diffusion via local or API)
- Stock footage fallback
- Ken Burns effect and motion
- Scene-matching algorithms

### 6. Video Assembler (`src/assemblers/video_assembler.py`)
Combines all elements:
- Voiceover synchronization
- Visual transitions
- Subtitle burning
- Background music and SFX
- Export to MP4 (9:16 vertical)

### 7. Metadata Generator (`src/generators/metadata_generator.py`)
Creates YouTube-ready metadata:
- Title variations
- Description with hashtags
- Thumbnail text suggestions
- Tags and categories

## 📝 Example Output

After running the demo, you'll find:

```
projects/demo_project/
├── script/
│   ├── script.json          # Full script with scenes
│   └── script.txt           # Plain text version
├── audio/
│   ├── narration.wav        # Voiceover audio
│   └── background.mp3       # Background music
├── visuals/
│   ├── scene_001.png        # Generated images
│   ├── scene_002.png
│   └── ...
├── subtitles/
│   ├── subtitles.srt        # Subtitle file
│   └── subtitles_ass.ass    # Styled subtitles
├── output/
│   └── final_video.mp4      # Ready-to-upload video
├── metadata/
│   ├── titles.txt           # Title variations
│   ├── description.txt      # Video description
│   └── tags.txt             # Hashtags and tags
└── project_config.yaml      # Project-specific config
```

## 🎨 Customization

### Adding New Niches
Edit `src/generators/topic_generator.py` and add your niche to the `NICHES` dictionary.

### Custom Voice Selection
Modify `config.yaml` under the `tts` section to change voice, speed, or pitch.

### Visual Style Presets
Create custom visual presets in `config.yaml` under the `visuals` section.

### Prompt Templates
Edit prompt templates in `templates/` to customize script style and tone.

## ⚠️ Important Notes

### Licensing & Copyright
- All generated content should be original
- Use only royalty-free or properly licensed stock media
- Background music should be from copyright-free sources
- AI-generated visuals are generally safe for commercial use
- Always verify licensing for any third-party assets

### Legal Disclaimer
This tool is designed to help creators produce original content. Do not:
- Copy existing creators' exact scripts, voice, or branding
- Use copyrighted material without permission
- Impersonate real individuals
- Spread misinformation

Focus on creating educational, entertaining, and original content.

## 🐛 Troubleshooting

### Common Issues

**FFmpeg not found**: Ensure FFmpeg is installed and added to your system PATH.

**TTS errors**: Try switching TTS engines in `config.yaml`. Some require internet connection.

**Out of memory**: Reduce resolution or use CPU-only mode for AI generation.

**Slow generation**: Use lightweight models or reduce video duration.

### Performance Tips

- Use GPU acceleration if available
- Lower resolution for faster rendering
- Use cached assets when possible
- Run during off-peak hours for API-based services

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by high-retention educational short-form content creators
- Built with love for the creator community
- Thanks to all open-source contributors whose tools make this possible

---

**Ready to create viral content?** Start with the demo:

```bash
python src/main.py --demo
```

For more help, run:
```bash
python src/main.py --help
```
