# Gradio Web Interface for Faceless Viral Video Bot

import gradio as gr
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config_manager import get_config
from src.generators.topic_generator import TopicGenerator
from src.generators.script_writer import ScriptWriter
from src.generators.metadata_generator import MetadataGenerator
from src.processors.voice_processor import VoiceProcessor
from src.processors.subtitle_processor import SubtitleProcessor
from src.processors.visual_processor import VisualProcessor

config = get_config()

def generate_pipeline(niche, duration, tone, voice_id, style_preset):
    """Run the full video generation pipeline"""
    try:
        project_name = f"web_{niche}_{tone}"
        base_path = Path("projects") / project_name
        base_path.mkdir(parents=True, exist_ok=True)
        
        # 1. Generate Topics
        topic_gen = TopicGenerator()
        ideas = topic_gen.generate_ideas(niche, count=3)
        selected_topic = ideas[0]['topic'] if ideas else f"Mystery of {niche}"
        
        topic_json = base_path / "script" / "topics.json"
        topic_json.parent.mkdir(parents=True, exist_ok=True)
        with open(topic_json, 'w') as f:
            json.dump(ideas, f, indent=2)
        
        # 2. Write Script
        script_writer = ScriptWriter()
        script_data = script_writer.write_script(selected_topic, duration, tone)
        
        script_file = base_path / "script" / "script.json"
        with open(script_file, 'w') as f:
            json.dump(script_data, f, indent=2)
        
        script_text = script_data.get('full_script', 'No script generated')
        
        # 3. Generate Voiceover
        voice_proc = VoiceProcessor()
        audio_path = base_path / "audio" / "narration.wav"
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Try to generate audio (might fail if TTS not installed)
        try:
            voice_proc.generate_voice(script_text, str(audio_path), voice_id)
            audio_status = "✅ Audio generated"
        except Exception as e:
            audio_status = f"⚠️ Audio skipped: {str(e)}"
        
        # 4. Generate Subtitles
        sub_proc = SubtitleProcessor()
        scenes = script_data.get('scenes', [])
        
        srt_path = base_path / "subtitles" / "subs.srt"
        ass_path = base_path / "subtitles" / "subs.ass"
        srt_path.parent.mkdir(parents=True, exist_ok=True)
        
        sub_proc.generate_srt(scenes, str(srt_path))
        sub_proc.generate_ass(scenes, str(ass_path), style_preset)
        
        # 5. Generate Visuals
        vis_proc = VisualProcessor()
        visuals_path = base_path / "visuals"
        visuals_path.mkdir(parents=True, exist_ok=True)
        
        generated_visuals = []
        for i, scene in enumerate(scenes):
            visual_path = visuals_path / f"scene_{i+1:03d}.png"
            emotion = scene.get('emotion', 'neutral')
            vis_proc.create_gradient_background(str(visual_path), emotion)
            generated_visuals.append(str(visual_path))
        
        # 6. Generate Metadata
        meta_gen = MetadataGenerator()
        metadata = meta_gen.generate_metadata(selected_topic, script_text, niche)
        
        meta_file = base_path / "metadata" / "metadata.json"
        meta_file.parent.mkdir(parents=True, exist_ok=True)
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Format output
        output = f"""
### ✅ Generation Complete!

**Project:** `{project_name}`
**Topic:** {selected_topic}
**Duration:** {duration}s
**Tone:** {tone}

---

### 📝 Script Preview:
{script_text[:500]}{'...' if len(script_text) > 500 else ''}

---

### 🎵 Audio Status:
{audio_status}

---

### 🎬 Visuals Generated:
{len(generated_visuals)} scenes created in `{visuals_path}`

---

### 🏷️ Title Suggestions:
{chr(10).join(['- ' + t for t in metadata.get('youtube_titles', [])[:3]])}

### #️⃣ Hashtags:
{' '.join(metadata.get('hashtags', [])[:5])}

---

📂 **Files saved to:** `{base_path.absolute()}`
        """
        
        return output, str(base_path.absolute())
        
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

# Create Gradio Interface
with gr.Blocks(title="Faceless Viral Video Bot") as demo:
    gr.Markdown("""
    # 🎬 Faceless Viral Video Bot
    ### AI-Powered YouTube Shorts Automation
    
    Generate complete viral-style videos with scripts, voiceovers, subtitles, and visuals automatically.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Configuration")
            
            niche_input = gr.Dropdown(
                choices=["facts", "history", "science", "mysteries", "finance", "what_if"],
                value="science",
                label="Niche"
            )
            
            duration_input = gr.Slider(
                minimum=20,
                maximum=60,
                value=45,
                step=5,
                label="Duration (seconds)"
            )
            
            tone_input = gr.Dropdown(
                choices=["dramatic", "curious", "educational", "mysterious", "energetic"],
                value="curious",
                label="Tone"
            )
            
            voice_input = gr.Dropdown(
                choices=["en-US-JennyNeural", "en-US-GuyNeural", "en-GB-SoniaNeural"],
                value="en-US-JennyNeural",
                label="Voice ID"
            )
            
            style_input = gr.Dropdown(
                choices=["modern", "classic", "minimal"],
                value="modern",
                label="Subtitle Style"
            )
            
            generate_btn = gr.Button("🚀 Generate Video", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Output")
            output_text = gr.Textbox(label="Generation Results", lines=20)
            output_path = gr.Textbox(label="Project Location", interactive=False)
    
    gr.Markdown("""
    ---
    ### 💡 Tips:
    - Select a niche to get relevant topics
    - Adjust duration for Shorts (20-60s)
    - Different tones affect script pacing
    - Check the project folder for all generated assets
    """)
    
    generate_btn.click(
        fn=generate_pipeline,
        inputs=[niche_input, duration_input, tone_input, voice_input, style_input],
        outputs=[output_text, output_path]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
