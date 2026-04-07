"""
Topic and idea generator for viral short-form content.
Generates engaging topics based on selected niche.
"""

import json
import csv
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Predefined topic templates for each niche (fallback when LLM not available)
NICHES = {
    "facts": {
        "templates": [
            "The shocking truth about {topic} that nobody tells you",
            "Why {topic} is more dangerous than you think",
            "The hidden secret behind {topic}",
            "What they don't want you to know about {topic}",
            "The real reason why {topic} exists"
        ],
        "topics": [
            "sleep", "sugar", "social media", "coffee", "exercise",
            "memory", "dreams", "bacteria", "gravity", "time"
        ]
    },
    "history": {
        "templates": [
            "The untold story of {topic}",
            "How {topic} changed the world forever",
            "The darkest secret of {topic}",
            "Why {topic} was erased from history books",
            "The conspiracy behind {topic}"
        ],
        "topics": [
            "ancient rome", "vikings", "medieval times", "world war 2",
            "ancient egypt", "the renaissance", "the cold war", "pirates"
        ]
    },
    "science": {
        "templates": [
            "Scientists just discovered something shocking about {topic}",
            "The mind-blowing truth about {topic}",
            "Why {topic} breaks the laws of physics",
            "The terrifying science behind {topic}",
            "What happens when {topic} goes wrong"
        ],
        "topics": [
            "black holes", "quantum mechanics", "dna", "consciousness",
            "dark matter", "artificial intelligence", "climate change", "viruses"
        ]
    },
    "mysteries": {
        "templates": [
            "The unsolved mystery of {topic}",
            "What really happened to {topic}?",
            "The conspiracy theory about {topic} that might be true",
            "The disturbing truth about {topic}",
            "Why {topic} remains a mystery after all these years"
        ],
        "topics": [
            "bermuda triangle", "area 51", "lost civilizations", "cryptids",
            "haunted places", "disappearances", "ancient aliens", "secret societies"
        ]
    },
    "finance": {
        "templates": [
            "The dark truth about {topic} that banks hide",
            "Why {topic} will make you rich (or broke)",
            "The secret strategy billionaires use with {topic}",
            "How {topic} controls your money",
            "The shocking reality of {topic}"
        ],
        "topics": [
            "credit cards", "stocks", "real estate", "crypto", "inflation",
            "taxes", "retirement", "debt", "investing", "banking"
        ]
    },
    "what_if": {
        "templates": [
            "What if {topic} suddenly disappeared?",
            "What would happen if {topic} was illegal?",
            "What if everyone had access to {topic}?",
            "What if {topic} never existed?",
            "What happens when {topic} becomes reality?"
        ],
        "topics": [
            "money", "internet", "electricity", "governments", "oceans",
            "bees", "sunlight", "oxygen", "technology", "death"
        ]
    }
}


class TopicGenerator:
    """Generate viral topic ideas for short-form content."""
    
    def __init__(self, niche: str = "science"):
        """
        Initialize topic generator.
        
        Args:
            niche: Content niche (facts, history, science, mysteries, finance, what_if)
        """
        self.niche = niche.lower()
        if self.niche not in NICHES:
            logger.warning(f"Unknown niche '{niche}'. Using 'facts' as fallback.")
            self.niche = "facts"
        
        self.generated_ideas: List[Dict[str, Any]] = []
    
    def generate_ideas(self, count: int = 10, use_llm: bool = False) -> List[Dict[str, Any]]:
        """
        Generate viral topic ideas.
        
        Args:
            count: Number of ideas to generate
            use_llm: Whether to use LLM for generation (if available)
            
        Returns:
            List of topic ideas with metadata
        """
        if use_llm:
            # Try to use LLM if available
            try:
                ideas = self._generate_with_llm(count)
                if ideas:
                    self.generated_ideas = ideas
                    return ideas
            except Exception as e:
                logger.warning(f"LLM generation failed: {e}. Using template-based generation.")
        
        # Fallback to template-based generation
        ideas = self._generate_from_templates(count)
        self.generated_ideas = ideas
        return ideas
    
    def _generate_from_templates(self, count: int) -> List[Dict[str, Any]]:
        """Generate ideas using predefined templates."""
        niche_data = NICHES[self.niche]
        templates = niche_data["templates"]
        topics = niche_data["topics"]
        
        ideas = []
        used_combinations = set()
        
        for i in range(count):
            # Select random template and topic
            template = random.choice(templates)
            topic = random.choice(topics)
            
            # Ensure unique combinations
            combination = (template, topic)
            attempts = 0
            while combination in used_combinations and attempts < 10:
                template = random.choice(templates)
                topic = random.choice(topics)
                combination = (template, topic)
                attempts += 1
            
            if combination in used_combinations:
                continue
            
            used_combinations.add(combination)
            
            # Create title
            title = template.format(topic=topic.title())
            
            idea = {
                "id": i + 1,
                "title": title,
                "niche": self.niche,
                "topic_keyword": topic,
                "hook_potential": random.randint(7, 10),  # Estimated hook strength
                "virality_score": random.uniform(6.5, 9.5),
                "generated_at": datetime.now().isoformat(),
                "method": "template"
            }
            
            ideas.append(idea)
            logger.debug(f"Generated idea: {title}")
        
        return ideas
    
    def _generate_with_llm(self, count: int) -> List[Dict[str, Any]]:
        """
        Generate ideas using LLM (placeholder for actual implementation).
        
        This method should be connected to an actual LLM service like Ollama,
        Hugging Face, or OpenAI when available.
        
        Args:
            count: Number of ideas to generate
            
        Returns:
            List of topic ideas
        """
        # Placeholder - in production, this would call an actual LLM
        logger.info("LLM generation requested but not configured. Using template fallback.")
        return []
    
    def save_to_json(self, filepath: str, ideas: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Save generated ideas to JSON file.
        
        Args:
            filepath: Path to save JSON file
            ideas: Ideas to save (uses generated_ideas if None)
            
        Returns:
            Path to saved file
        """
        ideas_to_save = ideas if ideas else self.generated_ideas
        
        if not ideas_to_save:
            logger.warning("No ideas to save")
            return ""
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ideas_to_save, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(ideas_to_save)} ideas to {path}")
        return str(path)
    
    def save_to_csv(self, filepath: str, ideas: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Save generated ideas to CSV file.
        
        Args:
            filepath: Path to save CSV file
            ideas: Ideas to save (uses generated_ideas if None)
            
        Returns:
            Path to saved file
        """
        ideas_to_save = ideas if ideas else self.generated_ideas
        
        if not ideas_to_save:
            logger.warning("No ideas to save")
            return ""
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Define CSV columns
        fieldnames = ['id', 'title', 'niche', 'topic_keyword', 
                     'hook_potential', 'virality_score', 'generated_at', 'method']
        
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ideas_to_save)
        
        logger.info(f"Saved {len(ideas_to_save)} ideas to {path}")
        return str(path)
    
    def get_best_idea(self) -> Optional[Dict[str, Any]]:
        """
        Get the idea with highest virality score.
        
        Returns:
            Best idea or None if no ideas generated
        """
        if not self.generated_ideas:
            return None
        
        return max(self.generated_ideas, key=lambda x: x.get('virality_score', 0))
    
    def filter_by_score(self, min_score: float = 8.0) -> List[Dict[str, Any]]:
        """
        Filter ideas by minimum virality score.
        
        Args:
            min_score: Minimum virality score threshold
            
        Returns:
            Filtered list of ideas
        """
        return [idea for idea in self.generated_ideas 
                if idea.get('virality_score', 0) >= min_score]


def generate_topics(niche: str = "science", count: int = 10, 
                   output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to generate and save topics.
    
    Args:
        niche: Content niche
        count: Number of ideas to generate
        output_dir: Directory to save output files
        
    Returns:
        Dictionary with generation results
    """
    generator = TopicGenerator(niche)
    ideas = generator.generate_ideas(count)
    
    result = {
        "niche": niche,
        "count": len(ideas),
        "ideas": ideas,
        "best_idea": generator.get_best_idea(),
        "files": {}
    }
    
    if output_dir and ideas:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save to both JSON and CSV
        json_path = output_path / "topic_ideas.json"
        csv_path = output_path / "topic_ideas.csv"
        
        result["files"]["json"] = generator.save_to_json(str(json_path))
        result["files"]["csv"] = generator.save_to_csv(str(csv_path))
    
    return result


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Generating topic ideas for 'science' niche...")
    result = generate_topics("science", count=5, output_dir="projects/demo_project/script")
    
    print(f"\nGenerated {result['count']} ideas:")
    for idea in result['ideas'][:3]:
        print(f"  - {idea['title']} (Score: {idea['virality_score']:.1f})")
    
    if result['best_idea']:
        print(f"\nBest idea: {result['best_idea']['title']}")
