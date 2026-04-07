"""
Visual processor for generating and processing video visuals.
Supports AI generation, stock footage, and motion effects.
"""

import random
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class VisualProcessor:
    """Generate and process visuals for videos."""
    
    def __init__(self, style: str = "mixed", use_ai: bool = False):
        """
        Initialize visual processor.
        
        Args:
            style: Visual style (ai_generated, stock, mixed)
            use_ai: Whether to use AI image generation
        """
        self.style = style.lower()
        self.use_ai = use_ai
        
        # Color palettes for fallback backgrounds
        self.color_palettes = {
            "vibrant": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"],
            "cinematic": ["#1a1a2e", "#16213e", "#0f3460", "#533483", "#2c3e50"],
            "neutral": ["#f5f5f5", "#e0e0e0", "#bdbdbd", "#9e9e9e", "#757575"]
        }
    
    def generate_visuals_for_scenes(
        self,
        scenes: List[Dict[str, Any]],
        output_dir: str,
        topic: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Generate or source visuals for each scene.
        
        Args:
            scenes: List of scene dictionaries
            output_dir: Directory to save visual files
            topic: Video topic for context
            
        Returns:
            List of visual file paths mapped to scenes
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        visuals = []
        
        for i, scene in enumerate(scenes):
            visual_info = self._generate_scene_visual(
                scene,
                output_path,
                i + 1,
                topic
            )
            visuals.append(visual_info)
        
        return visuals
    
    def _generate_scene_visual(
        self,
        scene: Dict[str, Any],
        output_path: Path,
        scene_number: int,
        topic: str
    ) -> Dict[str, Any]:
        """Generate visual for a single scene."""
        
        keywords = scene.get('keywords', [])
        emotion = scene.get('emotion', 'neutral')
        
        # Try AI generation first if enabled
        if self.use_ai and self.style in ['ai_generated', 'mixed']:
            try:
                ai_image = self._generate_ai_image(
                    keywords, emotion, topic,
                    str(output_path / f"scene_{scene_number:03d}.png")
                )
                if ai_image:
                    return {
                        "scene_number": scene_number,
                        "type": "ai_generated",
                        "path": ai_image,
                        "prompt": self._create_prompt(keywords, emotion, topic),
                        "motion_effects": self._get_motion_effects(emotion)
                    }
            except Exception as e:
                logger.warning(f"AI generation failed: {e}. Using fallback.")
        
        # Fallback to generated placeholder images
        placeholder = self._generate_placeholder_image(
            keywords, emotion, topic,
            str(output_path / f"scene_{scene_number:03d}.png")
        )
        
        return {
            "scene_number": scene_number,
            "type": "generated",
            "path": placeholder,
            "prompt": "",
            "motion_effects": self._get_motion_effects(emotion)
        }
    
    def _generate_ai_image(
        self,
        keywords: List[str],
        emotion: str,
        topic: str,
        output_path: str
    ) -> Optional[str]:
        """
        Generate image using AI (Stable Diffusion or similar).
        
        This is a placeholder - actual implementation would connect to
        Stable Diffusion, DALL-E, or other image generation APIs.
        """
        logger.info("AI image generation requested but not configured.")
        return None
    
    def _generate_placeholder_image(
        self,
        keywords: List[str],
        emotion: str,
        topic: str,
        output_path: str
    ) -> str:
        """
        Generate a placeholder image with gradient background and text.
        
        Args:
            keywords: Scene keywords
            emotion: Scene emotion
            topic: Video topic
            output_path: Path to save image
            
        Returns:
            Path to generated image
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create vertical image (9:16 aspect ratio)
            width = 1080
            height = 1920
            
            # Select color based on emotion
            palette = self._get_palette_for_emotion(emotion)
            color1 = random.choice(palette)
            color2 = random.choice(palette)
            
            # Create gradient background
            img = Image.new('RGB', (width, height), color=color1)
            draw = ImageDraw.Draw(img)
            
            # Draw gradient
            for y in range(height):
                r = int(self._interpolate_color(color1, color2, y / height))
                draw.line([(0, y), (width, y)], fill=r)
            
            # Add keyword text
            if keywords:
                main_keyword = keywords[0].title()
                
                # Try to use default font, fall back to basic font
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
                except:
                    font = ImageFont.load_default()
                
                # Calculate text position (center)
                text_bbox = draw.textbbox((0, 0), main_keyword, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                
                # Draw text with shadow
                shadow_offset = 4
                draw.text((x + shadow_offset, y + shadow_offset), main_keyword, 
                         fill='black', font=font)
                draw.text((x, y), main_keyword, fill='white', font=font)
            
            # Save image
            img.save(output_path, 'PNG', quality=95)
            
            logger.info(f"Generated placeholder image: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate placeholder image: {e}")
            
            # Last resort: create minimal valid PNG
            return self._create_minimal_png(output_path)
    
    def _create_minimal_png(self, output_path: str) -> str:
        """Create a minimal valid PNG file as last resort fallback."""
        try:
            from PIL import Image
            
            width = 1080
            height = 1920
            
            # Create solid color image
            color = random.choice(self.color_palettes["vibrant"])
            img = Image.new('RGB', (width, height), color=color)
            img.save(output_path, 'PNG')
            
            return output_path
        except Exception as e:
            logger.error(f"Failed to create minimal PNG: {e}")
            return output_path
    
    def _interpolate_color(self, color1: str, color2: str, factor: float) -> tuple:
        """Interpolate between two hex colors."""
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return (r, g, b)
    
    def _get_palette_for_emotion(self, emotion: str) -> List[str]:
        """Get color palette based on emotion."""
        if emotion in ['dramatic', 'excited']:
            return self.color_palettes["vibrant"]
        elif emotion in ['mysterious']:
            return self.color_palettes["cinematic"]
        else:
            return self.color_palettes["neutral"]
    
    def _get_motion_effects(self, emotion: str) -> Dict[str, float]:
        """Get motion effect parameters based on emotion."""
        base_effects = {
            "zoom_speed": 0.05,
            "pan_direction": random.choice(['left', 'right', 'up', 'down']),
            "pan_speed": 0.03,
            "transition": 'fade'
        }
        
        if emotion == 'dramatic':
            base_effects['zoom_speed'] = 0.08
            base_effects['transition'] = 'quick_fade'
        elif emotion == 'mysterious':
            base_effects['zoom_speed'] = 0.02
            base_effects['transition'] = 'slow_fade'
        elif emotion == 'excited':
            base_effects['zoom_speed'] = 0.1
            base_effects['transition'] = 'cut'
        
        return base_effects
    
    def apply_ken_burns_effect(
        self,
        image_path: str,
        output_path: str,
        duration: float,
        effects: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Apply Ken Burns effect (pan and zoom) to an image.
        
        This creates a video clip from a still image with motion.
        
        Args:
            image_path: Path to source image
            output_path: Path to save video clip
            duration: Duration of the clip in seconds
            effects: Motion effect parameters
            
        Returns:
            Path to generated video clip
        """
        logger.info(f"Applying Ken Burns effect: {image_path} -> {output_path}")
        
        # This would use MoviePy or FFmpeg to create the motion effect
        # For now, we'll just return the image path as a placeholder
        return image_path
    
    def download_stock_image(
        self,
        query: str,
        output_path: str,
        width: int = 1080,
        height: int = 1920
    ) -> Optional[str]:
        """
        Download stock image from free sources.
        
        This is a placeholder for integration with Pexels, Pixabay, etc.
        
        Args:
            query: Search query
            output_path: Path to save image
            width: Desired width
            height: Desired height
            
        Returns:
            Path to downloaded image or None
        """
        logger.info(f"Stock image download requested: '{query}'")
        logger.warning("Stock image API not configured. Using generated placeholder.")
        return None
    
    def _create_prompt(self, keywords: List[str], emotion: str, topic: str) -> str:
        """Create AI image generation prompt."""
        style_words = {
            'dramatic': 'dramatic lighting, high contrast, cinematic',
            'excited': 'vibrant colors, dynamic composition, energetic',
            'mysterious': 'moody atmosphere, shadows, enigmatic',
            'educational': 'clear, informative, clean design',
            'neutral': 'balanced lighting, professional, clear'
        }
        
        keyword_str = ', '.join(keywords[:3]) if keywords else topic
        style = style_words.get(emotion, style_words['neutral'])
        
        prompt = f"{keyword_str}, {style}, vertical composition, high quality, detailed"
        return prompt


def generate_visuals(
    scenes: List[Dict[str, Any]],
    output_dir: str,
    topic: str = "",
    style: str = "mixed"
) -> List[Dict[str, Any]]:
    """
    Convenience function to generate visuals for all scenes.
    
    Args:
        scenes: List of scene dictionaries
        output_dir: Directory to save visuals
        topic: Video topic
        style: Visual style
        
    Returns:
        List of visual information dictionaries
    """
    processor = VisualProcessor(style)
    return processor.generate_visuals_for_scenes(scenes, output_dir, topic)


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Testing visual generation...")
    
    demo_scenes = [
        {"keywords": ["space", "black hole"], "emotion": "dramatic"},
        {"keywords": ["science", "research"], "emotion": "educational"},
        {"keywords": ["discovery", "universe"], "emotion": "excited"}
    ]
    
    output_dir = "projects/demo_project/visuals"
    visuals = generate_visuals(demo_scenes, output_dir, topic="Space Mysteries")
    
    print(f"\nGenerated {len(visuals)} visuals:")
    for visual in visuals:
        print(f"  Scene {visual['scene_number']}: {visual['path']} ({visual['type']})")
