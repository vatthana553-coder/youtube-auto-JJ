"""
Metadata generator for YouTube/video platform optimization.
Creates titles, descriptions, tags, and thumbnail suggestions.
"""

import random
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class MetadataGenerator:
    """Generate video metadata for platform optimization."""
    
    def __init__(self, platform: str = "youtube"):
        """
        Initialize metadata generator.
        
        Args:
            platform: Target platform (youtube, tiktok, instagram)
        """
        self.platform = platform.lower()
        
        # Platform-specific configurations
        self.platform_config = {
            "youtube": {
                "max_title_length": 60,
                "description_length": 500,
                "tags_count": 15,
                "hashtag_count": 3
            },
            "tiktok": {
                "max_title_length": 100,
                "description_length": 2200,
                "tags_count": 5,
                "hashtag_count": 5
            },
            "instagram": {
                "max_title_length": 75,
                "description_length": 2200,
                "tags_count": 10,
                "hashtag_count": 10
            }
        }
    
    def generate_metadata(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete metadata for a video.
        
        Args:
            script: Script dictionary
            
        Returns:
            Complete metadata dictionary
        """
        config = self.platform_config.get(self.platform, self.platform_config["youtube"])
        
        title = script.get('title', 'Amazing Video')
        niche = script.get('niche', 'general')
        narration = script.get('narration', '')
        
        metadata = {
            "titles": self.generate_titles(title, niche),
            "description": self.generate_description(script, config["description_length"]),
            "tags": self.generate_tags(niche, config["tags_count"]),
            "hashtags": self.generate_hashtags(niche, config["hashtag_count"]),
            "thumbnail_text": self.generate_thumbnail_text(title),
            "category": self.suggest_category(niche)
        }
        
        return metadata
    
    def generate_titles(self, base_title: str, niche: str) -> List[str]:
        """Generate multiple title variations."""
        
        title_templates = {
            "science": [
                "Scientists Just Discovered Something {adjective} About {topic}",
                "The {adjective} Truth About {topic} That Changes Everything",
                "Why {topic} Is More {adjective} Than You Think",
                "What They Don't Tell You About {topic}",
                "The {adjective} Secret Behind {topic}"
            ],
            "history": [
                "The {adjective} Story of {topic} They Never Taught You",
                "How {topic} Changed the World Forever",
                "The Dark Secret of {topic}",
                "Why {topic} Was Erased from History",
                "The Untold Truth About {topic}"
            ],
            "facts": [
                "{adjective} Facts That Will Blow Your Mind",
                "The Truth About {topic} Nobody Talks About",
                "Why Everyone Is Wrong About {topic}",
                "What {topic} Actually Means",
                "The {adjective} Reality of {topic}"
            ],
            "mysteries": [
                "The Unsolved Mystery of {topic}",
                "What Really Happened to {topic}?",
                "The Disturbing Truth About {topic}",
                "Why {topic} Remains a Mystery",
                "The Conspiracy Behind {topic}"
            ],
            "finance": [
                "The {adjective} Truth About {topic}",
                "How {topic} Controls Your Money",
                "Why {topic} Will Make You Rich or Broke",
                "The Secret Banks Don't Want You to Know About {topic}",
                "What Billionaires Understand About {topic}"
            ],
            "what_if": [
                "What If {topic} Suddenly Disappeared?",
                "What Would Happen If {topic} Was Illegal?",
                "What If Everyone Had Access to {topic}?",
                "The Shocking Consequences of {topic}",
                "What Happens When {topic} Becomes Reality?"
            ]
        }
        
        adjectives = [
            "Shocking", "Mind-Blowing", "Terrifying", "Incredible",
            "Disturbing", "Amazing", "Unbelievable", "Hidden"
        ]
        
        templates = title_templates.get(niche, title_templates["facts"])
        titles = []
        
        for template in templates[:5]:
            title_variation = template.format(
                adjective=random.choice(adjectives),
                topic=base_title
            )
            
            # Truncate if too long
            if len(title_variation) > 60:
                title_variation = title_variation[:57] + "..."
            
            titles.append(title_variation)
        
        # Add original title
        if base_title not in titles:
            titles.insert(0, base_title)
        
        return titles
    
    def generate_description(self, script: Dict[str, Any], max_length: int = 500) -> str:
        """Generate video description."""
        
        title = script.get('title', 'Video')
        niche = script.get('niche', 'general')
        narration = script.get('narration', '')
        
        # Create description from narration summary
        first_sentence = narration.split('.')[0] if narration else title
        
        description_templates = [
            f"{first_sentence}. In this video, we explore the fascinating truth about {title}. "
            f"Watch until the end for a shocking revelation! \n\n"
            f"Don't forget to like, subscribe, and hit the notification bell for more "
            f"{niche} content!\n\n"
            f"#Shorts #{niche.replace('_', '')} #Viral",
            
            f"Discover the incredible secrets behind {title}. "
            f"{first_sentence} This will change how you see everything.\n\n"
            f"Subscribe for daily {niche} facts and mind-blowing discoveries!\n\n"
            f"#Shorts #Facts #Learning",
            
            f"The truth about {title} revealed! {first_sentence}\n\n"
            f"If you enjoyed this, check out our other videos on {niche}.\n\n"
            f"Like and subscribe for more!\n\n"
            f"#Shorts #Educational #Trending"
        ]
        
        description = random.choice(description_templates)
        
        # Truncate to max length
        if len(description) > max_length:
            description = description[:max_length - 3] + "..."
        
        return description
    
    def generate_tags(self, niche: str, count: int = 15) -> List[str]:
        """Generate relevant tags."""
        
        base_tags = {
            "science": ["science", "facts", "education", "learning", "discovery", 
                       "research", "scientific", "knowledge", "STEM", "physics",
                       "biology", "chemistry", "space", "universe", "nature"],
            "history": ["history", "historical", "past", "ancient", "civilization",
                       "historical facts", "education", "learning", "documentary",
                       "vintage", "retro", "classic", "heritage", "culture", "tradition"],
            "facts": ["facts", "trivia", "interesting facts", "did you know", "knowledge",
                     "learning", "education", "mind blowing", "amazing", "cool facts",
                     "random facts", "fun facts", "true facts", "daily facts", "fact check"],
            "mysteries": ["mystery", "unsolved", "conspiracy", "paranormal", "strange",
                         "unexplained", "mysterious", "creepy", "scary", "dark",
                         "secrets", "hidden truth", "cover up", "truth", "real mystery"],
            "finance": ["finance", "money", "investing", "wealth", "financial freedom",
                       "stocks", "crypto", "economy", "business", "entrepreneur",
                       "passive income", "rich", "millionaire", "financial tips", "banking"],
            "what_if": ["what if", "hypothetical", "scenario", "imagine", "thought experiment",
                       "alternative reality", "simulation", "theory", "speculation",
                       "possibility", "future", "predictions", "science fiction", "concept"]
        }
        
        tags = base_tags.get(niche, base_tags["facts"])
        
        # Add general viral tags
        general_tags = ["shorts", "viral", "trending", "fyp", "explore"]
        
        all_tags = tags + general_tags
        random.shuffle(all_tags)
        
        return all_tags[:count]
    
    def generate_hashtags(self, niche: str, count: int = 3) -> List[str]:
        """Generate hashtags for social media."""
        
        hashtag_map = {
            "science": ["#Science", "#Facts", "#Education", "#Learning", "#Discovery"],
            "history": ["#History", "#Historical", "#Past", "#Ancient", "#Heritage"],
            "facts": ["#Facts", "#Trivia", "#DidYouKnow", "#Knowledge", "#LearnSomethingNew"],
            "mysteries": ["#Mystery", "#Unsolved", "#Conspiracy", "#Paranormal", "#Strange"],
            "finance": ["#Finance", "#Money", "#Investing", "#Wealth", "#FinancialFreedom"],
            "what_if": ["#WhatIf", "#Hypothetical", "#Imagine", "#Theory", "#ThoughtExperiment"]
        }
        
        hashtags = hashtag_map.get(niche, hashtag_map["facts"])
        
        # Add platform-specific hashtags
        if self.platform == "youtube":
            hashtags.extend(["#Shorts", "#YouTubeShorts", "#Viral"])
        elif self.platform == "tiktok":
            hashtags.extend(["#fyp", "#foryou", "#viral", "#trending"])
        elif self.platform == "instagram":
            hashtags.extend(["#reels", "#instagram", "#explore"])
        
        return hashtags[:count]
    
    def generate_thumbnail_text(self, title: str) -> List[str]:
        """Generate short text options for thumbnails."""
        
        # Extract key words from title
        words = title.split()
        key_words = [w for w in words if len(w) > 4 and w.lower() not in 
                    ['about', 'that', 'this', 'with', 'from', 'have', 'been', 'were']]
        
        text_options = []
        
        # Create short phrases
        if key_words:
            text_options.append(" ".join(key_words[:3]).upper())
        
        # Add dramatic phrases
        dramatic_phrases = [
            "SHOCKING!",
            "MIND-BLOWING",
            "THE TRUTH",
            "REVEALED",
            "YOU WON'T BELIEVE",
            "GAME CHANGER",
            "EXPOSED",
            "SECRET REVEALED"
        ]
        
        text_options.extend(random.sample(dramatic_phrases, min(3, len(dramatic_phrases))))
        
        return text_options[:5]
    
    def suggest_category(self, niche: str) -> str:
        """Suggest video category."""
        
        category_map = {
            "science": "Education",
            "history": "Education",
            "facts": "Education",
            "mysteries": "Entertainment",
            "finance": "Education",
            "what_if": "Education"
        }
        
        return category_map.get(niche, "Education")
    
    def save_metadata(self, metadata: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Save metadata to files."""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = {}
        
        # Save titles
        titles_file = output_path / "titles.txt"
        with open(titles_file, 'w', encoding='utf-8') as f:
            f.write("TITLE VARIATIONS:\n\n")
            for i, title in enumerate(metadata.get('titles', []), 1):
                f.write(f"{i}. {title}\n")
        saved_files['titles'] = str(titles_file)
        
        # Save description
        desc_file = output_path / "description.txt"
        with open(desc_file, 'w', encoding='utf-8') as f:
            f.write(metadata.get('description', ''))
        saved_files['description'] = str(desc_file)
        
        # Save tags
        tags_file = output_path / "tags.txt"
        with open(tags_file, 'w', encoding='utf-8') as f:
            f.write("TAGS:\n")
            f.write(", ".join(metadata.get('tags', [])))
            f.write("\n\nHASHTAGS:\n")
            f.write(" ".join(metadata.get('hashtags', [])))
        saved_files['tags'] = str(tags_file)
        
        # Save thumbnail text
        thumb_file = output_path / "thumbnail_text.txt"
        with open(thumb_file, 'w', encoding='utf-8') as f:
            f.write("THUMBNAIL TEXT OPTIONS:\n\n")
            for text in metadata.get('thumbnail_text', []):
                f.write(f"- {text}\n")
        saved_files['thumbnail_text'] = str(thumb_file)
        
        # Save complete metadata as JSON
        import json
        json_file = output_path / "metadata.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        saved_files['json'] = str(json_file)
        
        logger.info(f"Saved metadata files to {output_dir}")
        return saved_files


def generate_video_metadata(
    script: Dict[str, Any],
    output_dir: str,
    platform: str = "youtube"
) -> Dict[str, Any]:
    """
    Convenience function to generate and save video metadata.
    
    Args:
        script: Script dictionary
        output_dir: Directory to save metadata
        platform: Target platform
        
    Returns:
        Generated metadata
    """
    generator = MetadataGenerator(platform)
    metadata = generator.generate_metadata(script)
    generator.save_metadata(metadata, output_dir)
    
    return metadata


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Testing metadata generation...")
    
    demo_script = {
        "title": "Black Holes",
        "niche": "science",
        "narration": "Black holes can bend time itself. Research shows these cosmic phenomena are even stranger than we thought."
    }
    
    output_dir = "projects/demo_project/metadata"
    metadata = generate_video_metadata(demo_script, output_dir, platform="youtube")
    
    print(f"\nGenerated metadata:")
    print(f"Titles: {metadata['titles'][:2]}")
    print(f"Hashtags: {metadata['hashtags']}")
    print(f"Category: {metadata['category']}")
