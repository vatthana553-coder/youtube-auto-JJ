import asyncio
import edge_tts
import os
import json

# Configuration
OUTPUT_DIR = "output"
VOICE = "en-US-GuyNeural"  # Deep, narrative voice similar to Zack D. Films
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_script_from_user():
    """
    In a real free setup without an API key, you might write the prompt yourself 
    or use a local LLM. For this script, we will structure the input for you.
    """
    print("--- Zack D. Films Style Generator ---")
    topic = input("Enter a weird fact or topic (e.g., 'What happens if you swallow gum'): ")
    
    # Prompt engineering for the specific style: Fast, punchy, visual descriptions
    system_prompt = f"""
    You are a scriptwriter for a viral YouTube Shorts channel like 'Zack D. Films'.
    Topic: {topic}
    
    Rules:
    1. Hook in the first 3 seconds.
    2. Keep sentences short and punchy (max 15 words per sentence).
    3. Total length under 50 seconds (approx 130 words).
    4. Tone: Curious, fast-paced, slightly mysterious.
    5. Output format: JSON list of objects with keys 'text' (spoken audio) and 'image_prompt' (detailed visual description for AI generator).
    
    Example Output Format:
    [
        {{"text": "Have you ever wondered what happens to gum in your stomach?", "image_prompt": "3d render, cute cartoon boy swallowing gum, cross section view of throat, bright lighting, pixar style"}},
        {{"text": "Most people think it stays there for 7 years.", "image_prompt": "3d render, calendar flipping rapidly, dust accumulating on a piece of gum, dark background"}},
        {{"text": "But that is a complete lie.", "image_prompt": "3d render, big red stamp saying FALSE, dramatic lighting, explosion effect"}}
    ]
    
    Generate the JSON only. No markdown formatting.
    """
    return system_prompt, topic

def mock_llm_generation(prompt):
    """
    Since we don't have a paid API key here, this function simulates the LLM output 
    or allows you to paste your own script if you run this locally with an LLM.
    
    TO MAKE THIS FULLY AUTOMATIC FOR FREE:
    1. Install Ollama (ollama.com)
    2. Run: ollama run llama3
    3. Uncomment the subprocess code below to call local Llama3.
    
    For now, we will create a template structure you can fill or connect to HuggingFace.
    """
    print("\n[INFO] In a real environment, this calls a free LLM (like Llama3 via Ollama or HuggingFace).")
    print("[INFO] Generating a sample structure for demonstration...")
    
    # SAMPLE DATA FOR DEMONSTRATION (Replace this with actual LLM call)
    sample_script = [
        {
            "text": "Have you ever wondered what actually happens to gum in your stomach?",
            "image_prompt": "3d render, cute cartoon boy swallowing gum, cross section view of throat, bright lighting, pixar style, 8k"
        },
        {
            "text": "Most people think it stays there for seven years.",
            "image_prompt": "3d render, old calendar flipping rapidly, dust accumulating on a piece of gum inside a stomach, dark moody lighting"
        },
        {
            "text": "But doctors say that is a complete lie.",
            "image_prompt": "3d render, doctor shaking head, big red text FALSE floating in air, dramatic studio lighting"
        },
        {
            "text": "Your body simply moves it through your digestive system normally.",
            "image_prompt": "3d render, animation of digestive tract, gum moving smoothly through intestines, clean medical illustration style"
        },
        {
            "text": "It comes out exactly the same way it went in, just a few days later.",
            "image_prompt": "3d render, toilet flushing, humorous but clean, bright bathroom lighting, pixar style"
        }
    ]
    return sample_script

async def generate_audio(text, output_file):
    """Generates MP3 using Edge TTS (Free, High Quality)"""
    communicate = edge_tts.Communicate(text, VOICE, rate="+10%", pitch="+0Hz")
    await communicate.save(output_file)
    print(f"✅ Audio generated: {output_file}")

async def main():
    # 1. Get Content
    _, topic = get_script_from_user()
    
    # 2. Generate Script (Simulated LLM)
    script_data = mock_llm_generation(topic)
    
    # Save script to JSON for reference
    script_path = os.path.join(OUTPUT_DIR, "script.json")
    with open(script_path, "w") as f:
        json.dump(script_data, f, indent=2)
    print(f"💾 Script saved to {script_path}")

    # 3. Generate Audio & Prepare Image Prompts
    print("\n🎙️ Generating Voiceover...")
    
    full_text = " ".join([item['text'] for item in script_data])
    audio_path = os.path.join(OUTPUT_DIR, "voiceover.mp3")
    
    # Generate one continuous audio file for the whole script
    await generate_audio(full_text, audio_path)
    
    # 4. Output Instructions for Visuals
    print("\n🎨 Next Steps for Visuals (Free Workflow):")
    print("-" * 40)
    print("Copy these prompts into Bing Image Creator (bing.com/images/create) or Leonardo.ai:")
    print("-" * 40)
    
    for i, scene in enumerate(script_data):
        print(f"\nScene {i+1}: \"{scene['text']}\"")
        print(f"Prompt: {scene['image_prompt']}")
        
    print("\n" + "="*40)
    print("EDITING INSTRUCTIONS:")
    print("1. Import 'voiceover.mp3' into CapCut.")
    print("2. Generate images using the prompts above.")
    print("3. Add 'Keyframe Animations' (Zoom in/Pan) to images to match Zack D. style.")
    print("4. Add auto-captions in CapCut with a bold font (like 'The Bold Font').")
    print("="*40)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess cancelled.")
