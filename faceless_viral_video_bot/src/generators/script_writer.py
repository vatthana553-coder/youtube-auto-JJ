"""
Script writer for viral short-form content.
Generates engaging scripts with hooks, buildup, and payoff structure.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Script structure templates
SCRIPT_TEMPLATES = {
    "hook_patterns": [
        "Did you know that {fact}?",
        "What if I told you {revelation}?",
        "The truth about {topic} will shock you.",
        "Everyone believes {myth}, but they're wrong.",
        "This one fact about {topic} changes everything.",
        "Scientists just discovered something terrifying about {topic}.",
        "You won't believe what {subject} actually does.",
        "The dark secret behind {topic} nobody talks about."
    ],
    "buildup_patterns": [
        "Here's what most people don't understand...",
        "Let me explain why this matters...",
        "The reason behind this is fascinating...",
        "But there's more to the story...",
        "What happens next will surprise you...",
        "This is where it gets really interesting..."
    ],
    "payoff_patterns": [
        "And that's the shocking truth about {topic}.",
        "Now you know the real story behind {topic}.",
        "This changes everything we thought we knew.",
        "The implications are mind-blowing.",
        "And that's why {topic} is more important than you realized.",
        "Share this before they delete it!"
    ]
}


# Sample content for different niches (fallback when LLM not available)
NICHE_CONTENT = {
    "science": {
        "facts": [
            "black holes can bend time itself",
            "your DNA is 99.9% identical to every other human",
            "quantum particles can exist in multiple places at once",
            "the universe is expanding faster than light speed",
            "consciousness might be a quantum phenomenon"
        ],
        "subjects": ["space", "biology", "physics", "chemistry", "neuroscience"],
        "myths": ["we only use 10% of our brain", "goldfish have 3-second memory"]
    },
    "history": {
        "facts": [
            "ancient Romans used urine as mouthwash",
            "the shortest war in history lasted only 38 minutes",
            "Vikings didn't actually wear horned helmets",
            "Napoleon wasn't actually short for his time",
            "the Library of Alexandria wasn't destroyed in a single fire"
        ],
        "subjects": ["ancient civilizations", "wars", "emperors", "discoveries", "cultures"],
        "myths": ["Columbus proved the Earth was round", "Medieval people thought the Earth was flat"]
    },
    "facts": {
        "facts": [
            "honey never spoils - archaeologists found edible honey in Egyptian tombs",
            "octopuses have three hearts and blue blood",
            "bananas are berries, but strawberries aren't",
            "your stomach lining replaces itself every few days",
            "there are more possible chess games than atoms in the universe"
        ],
        "subjects": ["nature", "human body", "animals", "food", "random facts"],
        "myths": ["shaving makes hair grow back thicker", "cracking knuckles causes arthritis"]
    },
    "mysteries": {
        "facts": [
            "the Bermuda Triangle has swallowed entire ships without a trace",
            "ancient civilizations built structures we still can't replicate",
            "some people claim to remember past lives with verifiable details",
            "cryptids like Bigfoot have thousands of eyewitness accounts",
            "certain haunted locations have consistent paranormal reports across centuries"
        ],
        "subjects": ["unsolved mysteries", "paranormal", "conspiracies", "ancient secrets", "disappearances"],
        "myths": ["all mysteries have rational explanations", "eyewitness testimony is reliable"]
    },
    "finance": {
        "facts": [
            "the average credit card user pays over $1000 yearly in interest alone",
            "billionaires often pay lower tax rates than middle-class workers",
            "compound interest can turn $100 monthly into over $1 million",
            "most millionaires drive used cars, not luxury vehicles",
            "the stock market has never had a negative 20-year period"
        ],
        "subjects": ["investing", "banking", "taxes", "wealth building", "money psychology"],
        "myths": ["you need lots of money to start investing", "credit cards are always bad"]
    },
    "what_if": {
        "facts": [
            "if bees disappeared, humans would have only 4 years left",
            "if the internet shut down, global economy would collapse in days",
            "if everyone jumped at once, Earth wouldn't move even a millimeter",
            "if oxygen doubled, insects would become gigantic",
            "if gravity stopped for a second, everything would fly into space"
        ],
        "subjects": ["nature", "technology", "physics", "biology", "society"],
        "myths": ["humans could survive without ecosystems", "technology makes us independent from nature"]
    }
}


class ScriptWriter:
    """Generate viral short-form video scripts."""
    
    def __init__(self, niche: str = "science", tone: str = "curious"):
        """
        Initialize script writer.
        
        Args:
            niche: Content niche
            tone: Tone of the script (curious, dramatic, educational, mysterious)
        """
        self.niche = niche.lower()
        self.tone = tone.lower()
        self.generated_scripts: List[Dict[str, Any]] = []
    
    def generate_script(
        self,
        topic: str,
        duration: int = 45,
        use_llm: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a complete script for a short-form video.
        
        Args:
            topic: Topic title or keyword
            duration: Target duration in seconds
            use_llm: Whether to use LLM for generation
            
        Returns:
            Complete script with scenes and timing
        """
        # Calculate word count based on duration (average 150 words per minute)
        words_per_minute = 150
        target_words = int((duration / 60) * words_per_minute)
        
        if use_llm:
            try:
                script = self._generate_with_llm(topic, duration)
                if script:
                    self.generated_scripts.append(script)
                    return script
            except Exception as e:
                logger.warning(f"LLM generation failed: {e}. Using template-based generation.")
        
        # Generate using templates
        script = self._generate_from_template(topic, duration, target_words)
        self.generated_scripts.append(script)
        return script
    
    def _generate_from_template(
        self,
        topic: str,
        duration: int,
        target_words: int
    ) -> Dict[str, Any]:
        """Generate script using predefined templates."""
        
        # Get niche-specific content
        niche_data = NICHE_CONTENT.get(self.niche, NICHE_CONTENT["facts"])
        
        # Select random elements
        hook_pattern = random.choice(SCRIPT_TEMPLATES["hook_patterns"])
        buildup_pattern = random.choice(SCRIPT_TEMPLATES["buildup_patterns"])
        payoff_pattern = random.choice(SCRIPT_TEMPLATES["payoff_patterns"])
        
        fact = random.choice(niche_data["facts"])
        subject = random.choice(niche_data["subjects"])
        
        # Create hook
        hook = hook_pattern.format(
            fact=fact,
            revelation=f"everything you know about {subject} is wrong",
            topic=topic.title(),
            myth=random.choice(niche_data.get("myths", ["common beliefs"])),
            subject=subject
        )
        
        # Create buildup content
        buildup_sentences = [
            buildup_pattern,
            f"Research shows that {fact.lower()},",
            f"Experts have been studying {subject} for decades,",
            f"What we've learned completely contradicts what we were taught,",
            f"The evidence is overwhelming and undeniable,"
        ]
        
        # Adjust number of sentences based on target length
        num_buildup = min(3, max(2, target_words // 50))
        buildup = " ".join(buildup_sentences[:num_buildup])
        
        # Create payoff
        payoff = payoff_pattern.format(topic=topic.lower())
        
        # Combine into full narration
        narration = f"{hook} {buildup} {payoff}"
        
        # Break into scenes
        scenes = self._create_scenes(narration, duration)
        
        # Calculate words per minute for duration estimate
        words_per_minute = 150
        
        # Create script object
        script = {
            "title": topic,
            "niche": self.niche,
            "tone": self.tone,
            "target_duration": duration,
            "target_words": target_words,
            "actual_words": len(narration.split()),
            "estimated_duration": len(narration.split()) / words_per_minute * 60,
            "narration": narration,
            "scenes": scenes,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "method": "template",
                "version": "1.0"
            }
        }
        
        logger.info(f"Generated script: {len(narration.split())} words, ~{script['estimated_duration']:.0f}s")
        return script
    
    def _create_scenes(self, narration: str, total_duration: int) -> List[Dict[str, Any]]:
        """Break narration into scenes with timestamps."""
        
        sentences = narration.replace(',', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        scenes = []
        total_time = 0
        
        for i, sentence in enumerate(sentences):
            # Calculate duration for this sentence
            words = len(sentence.split())
            sentence_duration = int((words / 150) * 60)  # Convert to seconds
            sentence_duration = max(2, min(sentence_duration, 8))  # Clamp between 2-8 seconds
            
            scene = {
                "scene_number": i + 1,
                "start_time": total_time,
                "end_time": total_time + sentence_duration,
                "duration": sentence_duration,
                "text": sentence,
                "visual_cue": self._get_visual_cue(sentence, i),
                "emotion": self._detect_emotion(sentence),
                "keywords": self._extract_keywords(sentence)
            }
            
            scenes.append(scene)
            total_time += sentence_duration
        
        # Adjust last scene to match total duration
        if scenes and total_time < total_duration:
            scenes[-1]["end_time"] = total_duration
            scenes[-1]["duration"] = total_duration - scenes[-1]["start_time"]
        
        return scenes
    
    def _get_visual_cue(self, text: str, scene_index: int) -> str:
        """Generate visual cue for a scene."""
        cues = [
            "dramatic zoom on subject",
            "quick cuts between related images",
            "slow pan across scene",
            "animated text overlay",
            "split screen comparison",
            "close-up detail shot",
            "wide establishing shot",
            "motion graphics illustration"
        ]
        return cues[scene_index % len(cues)]
    
    def _detect_emotion(self, text: str) -> str:
        """Detect emotional tone of text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["shock", "terrifying", "dark", "dangerous"]):
            return "dramatic"
        elif any(word in text_lower for word in ["fascinating", "amazing", "incredible", "mind-blowing"]):
            return "excited"
        elif any(word in text_lower for word in ["mystery", "secret", "unknown", "unsolved"]):
            return "mysterious"
        elif any(word in text_lower for word in ["truth", "fact", "research", "evidence"]):
            return "educational"
        else:
            return "neutral"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Simple keyword extraction (can be enhanced with NLP)
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", 
                     "being", "have", "has", "had", "do", "does", "did", "will", 
                     "would", "could", "should", "may", "might", "must", "shall"}
        
        words = text.lower().split()
        keywords = [word.strip(".,!?\"'") for word in words 
                   if word not in stop_words and len(word) > 3]
        
        return keywords[:5]  # Return top 5 keywords
    
    def _generate_with_llm(self, topic: str, duration: int) -> Optional[Dict[str, Any]]:
        """
        Generate script using LLM (placeholder for actual implementation).
        
        Args:
            topic: Topic for the script
            duration: Target duration
            
        Returns:
            Generated script or None
        """
        logger.info("LLM generation requested but not configured. Using template fallback.")
        return None
    
    def save_script(self, script: Dict[str, Any], filepath: str) -> str:
        """
        Save script to JSON file.
        
        Args:
            script: Script dictionary
            filepath: Path to save file
            
        Returns:
            Path to saved file
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved script to {path}")
        return str(path)
    
    def export_plain_text(self, script: Dict[str, Any], filepath: str) -> str:
        """
        Export script as plain text.
        
        Args:
            script: Script dictionary
            filepath: Path to save file
            
        Returns:
            Path to saved file
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"Title: {script['title']}\n")
            f.write(f"Niche: {script['niche']}\n")
            f.write(f"Tone: {script['tone']}\n")
            f.write(f"Duration: ~{script['estimated_duration']:.0f} seconds\n")
            f.write(f"Words: {script['actual_words']}\n\n")
            f.write("=" * 50 + "\n\n")
            f.write("FULL NARRATION:\n\n")
            f.write(script['narration'])
            f.write("\n\n")
            f.write("=" * 50 + "\n\n")
            f.write("SCENE BREAKDOWN:\n\n")
            
            for scene in script['scenes']:
                f.write(f"Scene {scene['scene_number']} ({scene['start_time']}-{scene['end_time']}s):\n")
                f.write(f"  Text: {scene['text']}\n")
                f.write(f"  Visual: {scene['visual_cue']}\n")
                f.write(f"  Emotion: {scene['emotion']}\n")
                f.write(f"  Keywords: {', '.join(scene['keywords'])}\n\n")
        
        logger.info(f"Exported plain text script to {path}")
        return str(path)


def write_script(
    topic: str,
    niche: str = "science",
    duration: int = 45,
    tone: str = "curious",
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to generate and save a script.
    
    Args:
        topic: Topic for the script
        niche: Content niche
        duration: Target duration
        tone: Script tone
        output_dir: Directory to save output files
        
    Returns:
        Generated script
    """
    writer = ScriptWriter(niche, tone)
    script = writer.generate_script(topic, duration)
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON version
        json_filename = f"script_{topic.lower().replace(' ', '_')}.json"
        writer.save_script(script, str(output_path / json_filename))
        
        # Save plain text version
        txt_filename = f"script_{topic.lower().replace(' ', '_')}.txt"
        writer.export_plain_text(script, str(output_path / txt_filename))
    
    return script


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Generating demo script...")
    script = write_script(
        topic="Black Holes",
        niche="science",
        duration=45,
        tone="dramatic",
        output_dir="projects/demo_project/script"
    )
    
    print(f"\nGenerated script:")
    print(f"Title: {script['title']}")
    print(f"Duration: ~{script['estimated_duration']:.0f}s")
    print(f"Words: {script['actual_words']}")
    print(f"\nNarration:\n{script['narration']}")
    print(f"\nScenes: {len(script['scenes'])}")
