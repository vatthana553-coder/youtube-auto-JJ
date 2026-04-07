"""
Subtitle processor for generating styled captions.
Creates SRT and ASS subtitle files with animations.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class SubtitleProcessor:
    """Generate and style subtitles for videos."""
    
    def __init__(self, style: str = "modern"):
        """
        Initialize subtitle processor.
        
        Args:
            style: Subtitle style (modern, classic, minimal)
        """
        self.style = style.lower()
        self.styles = {
            "modern": {
                "font": "Arial",
                "font_size": 48,
                "primary_color": "&H00FFFFFF",
                "secondary_color": "&H0000FFFF",
                "outline_color": "&H00000000",
                "back_color": "&H00000000",
                "bold": True,
                "italic": False,
                "underline": False,
                "strikeout": False,
                "shadow": 2,
                "border": 2,
                "alignment": 2,  # Bottom center
                "margin_v": 50,
                "margin_l": 20,
                "margin_r": 20
            },
            "classic": {
                "font": "Times New Roman",
                "font_size": 42,
                "primary_color": "&H00FFFF00",
                "secondary_color": "&H0000FFFF",
                "outline_color": "&H00000000",
                "back_color": "&H00000000",
                "bold": False,
                "italic": False,
                "underline": False,
                "strikeout": False,
                "shadow": 1,
                "border": 1,
                "alignment": 2,
                "margin_v": 40,
                "margin_l": 30,
                "margin_r": 30
            },
            "minimal": {
                "font": "Helvetica",
                "font_size": 36,
                "primary_color": "&H00FFFFFF",
                "secondary_color": "&H0000FFFF",
                "outline_color": "&H00000000",
                "back_color": "&H00000000",
                "bold": False,
                "italic": False,
                "underline": False,
                "strikeout": False,
                "shadow": 0,
                "border": 0,
                "alignment": 2,
                "margin_v": 60,
                "margin_l": 40,
                "margin_r": 40
            }
        }
    
    def generate_srt(self, scenes: List[Dict[str, Any]], output_path: str) -> str:
        """
        Generate SRT subtitle file from scenes.
        
        Args:
            scenes: List of scene dictionaries with text and timing
            output_path: Path to save SRT file
            
        Returns:
            Path to generated SRT file
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            for i, scene in enumerate(scenes, 1):
                # Convert seconds to SRT timestamp format
                start_time = self._seconds_to_srt_time(scene['start_time'])
                end_time = self._seconds_to_srt_time(scene['end_time'])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{scene['text']}\n\n")
        
        logger.info(f"Generated SRT subtitles: {path}")
        return str(path)
    
    def generate_ass(self, scenes: List[Dict[str, Any]], output_path: str, 
                     video_width: int = 1080, video_height: int = 1920) -> str:
        """
        Generate ASS subtitle file with styling and animations.
        
        Args:
            scenes: List of scene dictionaries
            output_path: Path to save ASS file
            video_width: Video width for positioning
            video_height: Video height for positioning
            
        Returns:
            Path to generated ASS file
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        style = self.styles.get(self.style, self.styles["modern"])
        
        with open(path, 'w', encoding='utf-8') as f:
            # Write ASS header
            f.write("[Script Info]\n")
            f.write(f"Title: Faceless Viral Video Subtitles\n")
            f.write(f"ScriptType: v4.00+\n")
            f.write(f"PlayResX: {video_width}\n")
            f.write(f"PlayResY: {video_height}\n")
            f.write(f"Timer: 100.0000\n\n")
            
            # Write styles
            f.write("[V4+ Styles]\n")
            f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, ")
            f.write("OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ")
            f.write("ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, ")
            f.write("Alignment, MarginL, MarginR, MarginV, Encoding\n")
            
            f.write(f"Style: Default,{style['font']},{style['font_size']},")
            f.write(f"{style['primary_color']},{style['secondary_color']},")
            f.write(f"{style['outline_color']},{style['back_color']},")
            f.write(f"{1 if style['bold'] else 0},{1 if style['italic'] else 0},")
            f.write(f"{1 if style['underline'] else 0},{1 if style['strikeout'] else 0},")
            f.write(f"100,100,0,0,1,{style['border']},{style['shadow']},")
            f.write(f"{style['alignment']},{style['margin_l']},{style['margin_r']},")
            f.write(f"{style['margin_v']},1\n\n")
            
            # Write events
            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, ")
            f.write("Effect, Text\n")
            
            for scene in scenes:
                start_time = self._seconds_to_ass_time(scene['start_time'])
                end_time = self._seconds_to_ass_time(scene['end_time'])
                
                # Add simple animation effect (fade in/out)
                text = self._format_text_for_ass(scene['text'], style)
                
                f.write(f"Dialogue: 0,{start_time},{end_time},Default,,")
                f.write(f"{style['margin_l']},{style['margin_r']},{style['margin_v']},")
                f.write(f",,{text}\n")
        
        logger.info(f"Generated ASS subtitles: {path}")
        return str(path)
    
    def _format_text_for_ass(self, text: str, style: Dict) -> str:
        """Format text with ASS tags for styling."""
        # Escape special characters
        text = text.replace('{', r'\{').replace('}', r'\}')
        
        # Add bold tags if needed
        if style['bold']:
            text = r'{\b1}' + text + r'{\b0}'
        
        return text
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _seconds_to_ass_time(self, seconds: float) -> str:
        """Convert seconds to ASS timestamp format (H:MM:SS.cc)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centiseconds = int((seconds - int(seconds)) * 100)
        
        return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"
    
    def generate_word_level_srt(self, words: List[Dict[str, Any]], output_path: str) -> str:
        """
        Generate word-level SRT subtitles.
        
        Args:
            words: List of word dictionaries with timing
            output_path: Path to save SRT file
            
        Returns:
            Path to generated SRT file
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            for i, word_data in enumerate(words, 1):
                start_time = self._seconds_to_srt_time(word_data['start'])
                end_time = self._seconds_to_srt_time(word_data['end'])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{word_data['text']}\n\n")
        
        logger.info(f"Generated word-level SRT: {path}")
        return str(path)
    
    def highlight_keywords(self, text: str, keywords: List[str]) -> str:
        """
        Add highlighting markup to keywords in text.
        
        Args:
            text: Original text
            keywords: Keywords to highlight
            
        Returns:
            Text with highlighted keywords
        """
        result = text
        for keyword in keywords:
            if keyword.lower() in result.lower():
                # Simple case-insensitive replacement
                result = result.replace(keyword, f"{{{keyword}}}")
        
        return result


def generate_subtitles(
    scenes: List[Dict[str, Any]],
    output_dir: str,
    style: str = "modern",
    formats: List[str] = None
) -> Dict[str, str]:
    """
    Convenience function to generate subtitles in multiple formats.
    
    Args:
        scenes: List of scene dictionaries
        output_dir: Directory to save subtitle files
        style: Subtitle style
        formats: List of formats to generate (default: ['srt', 'ass'])
        
    Returns:
        Dictionary of format to file path
    """
    if formats is None:
        formats = ['srt', 'ass']
    
    processor = SubtitleProcessor(style)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    if 'srt' in formats:
        srt_path = output_path / "subtitles.srt"
        results['srt'] = processor.generate_srt(scenes, str(srt_path))
    
    if 'ass' in formats:
        ass_path = output_path / "subtitles.ass"
        results['ass'] = processor.generate_ass(scenes, str(ass_path))
    
    return results


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Testing subtitle generation...")
    
    demo_scenes = [
        {"start_time": 0.0, "end_time": 3.5, "text": "Did you know this shocking fact?"},
        {"start_time": 3.5, "end_time": 7.0, "text": "Research shows something amazing."},
        {"start_time": 7.0, "end_time": 10.0, "text": "This changes everything we knew."}
    ]
    
    output_dir = "projects/demo_project/subtitles"
    results = generate_subtitles(demo_scenes, output_dir, style="modern")
    
    print(f"\nGenerated subtitles:")
    for fmt, path in results.items():
        print(f"  {fmt.upper()}: {path}")
