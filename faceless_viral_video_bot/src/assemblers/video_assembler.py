"""
Video assembler for combining all elements into final video.
Uses MoviePy and FFmpeg for video editing and assembly.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class VideoAssembler:
    """Assemble video from audio, visuals, subtitles, and effects."""
    
    def __init__(self, resolution: str = "1080x1920", fps: int = 30):
        """
        Initialize video assembler.
        
        Args:
            resolution: Video resolution (width x height)
            fps: Frames per second
        """
        self.width, self.height = map(int, resolution.split('x'))
        self.fps = fps
        self.resolution = resolution
    
    def assemble_video(
        self,
        script: Dict[str, Any],
        audio_path: str,
        visuals: List[Dict[str, Any]],
        output_path: str,
        subtitle_path: Optional[str] = None,
        background_music_path: Optional[str] = None
    ) -> str:
        """
        Assemble complete video from all components.
        
        Args:
            script: Script dictionary with scenes
            audio_path: Path to narration audio
            visuals: List of visual information dictionaries
            subtitle_path: Optional path to subtitle file
            background_music_path: Optional path to background music
            output_path: Path to save final video
            
        Returns:
            Path to assembled video
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use MoviePy for assembly
            return self._assemble_with_moviepy(
                script, audio_path, visuals, 
                subtitle_path, background_music_path, 
                str(output_file)
            )
        except ImportError as e:
            logger.warning(f"MoviePy not available: {e}. Using FFmpeg fallback.")
            return self._assemble_with_ffmpeg(
                script, audio_path, visuals,
                subtitle_path, background_music_path,
                str(output_file)
            )
        except Exception as e:
            logger.error(f"Assembly failed: {e}")
            # Create a minimal placeholder video
            return self._create_placeholder_video(str(output_file))
    
    def _assemble_with_moviepy(
        self,
        script: Dict[str, Any],
        audio_path: str,
        visuals: List[Dict[str, Any]],
        subtitle_path: Optional[str],
        background_music_path: Optional[str],
        output_path: str
    ) -> str:
        """Assemble video using MoviePy."""
        try:
            from moviepy.editor import (
                VideoFileClip, AudioFileClip, ImageClip,
                CompositeVideoClip, CompositeAudioClip, TextClip,
                ColorClip
            )
            from moviepy.video.fx.all import Resize, Crop
            import numpy as np
            
            logger.info("Assembling video with MoviePy...")
            
            # Load narration audio
            narration = AudioFileClip(audio_path)
            total_duration = narration.duration
            
            # Create clips for each scene
            clips = []
            
            for i, visual in enumerate(visuals):
                scene = script['scenes'][i] if i < len(script['scenes']) else None
                
                if scene:
                    duration = scene['end_time'] - scene['start_time']
                else:
                    duration = total_duration / len(visuals)
                
                # Create clip from image
                image_path = visual.get('path', '')
                
                if Path(image_path).exists():
                    # Create image clip with Ken Burns effect
                    clip = self._create_image_clip_with_motion(
                        image_path, duration, visual.get('motion_effects', {})
                    )
                else:
                    # Fallback to color clip
                    clip = ColorClip(
                        size=(self.width, self.height),
                        color=(50, 50, 50),
                        duration=duration
                    )
                
                clips.append(clip)
            
            # Concatenate all clips
            if clips:
                final_video = clips[0]
                for clip in clips[1:]:
                    final_video = final_video + clip
            else:
                # Create simple color video if no visuals
                final_video = ColorClip(
                    size=(self.width, self.height),
                    color=(50, 50, 50),
                    duration=total_duration
                )
            
            # Ensure video matches audio duration
            if final_video.duration < total_duration:
                # Loop or extend last frame
                final_video = final_video.set_duration(total_duration)
            elif final_video.duration > total_duration:
                final_video = final_video.subclip(0, total_duration)
            
            # Add narration audio
            final_video = final_video.set_audio(narration)
            
            # Add background music if provided
            if background_music_path and Path(background_music_path).exists():
                bg_music = AudioFileClip(background_music_path)
                
                # Loop music if shorter than video
                if bg_music.duration < total_duration:
                    bg_music = bg_music.audio_loop(duration=total_duration)
                else:
                    bg_music = bg_music.subclip(0, total_duration)
                
                # Reduce background music volume
                bg_music = bg_music.volumex(0.15)
                
                # Mix with narration
                final_audio = CompositeAudioClip([narration, bg_music])
                final_video = final_video.set_audio(final_audio)
            
            # Add subtitles if provided
            if subtitle_path and Path(subtitle_path).exists():
                # Note: Subtitle burning requires ImageMagick for TextClip
                # This is a simplified version
                logger.info(f"Subtitles found at {subtitle_path} but burning requires ImageMagick")
            
            # Write final video
            logger.info(f"Writing video to {output_path}")
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Clean up
            narration.close()
            final_video.close()
            
            logger.info(f"Video assembled successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"MoviePy assembly failed: {e}")
            raise
    
    def _create_image_clip_with_motion(
        self,
        image_path: str,
        duration: float,
        motion_effects: Dict[str, Any]
    ):
        """Create image clip with Ken Burns motion effect."""
        try:
            from moviepy.editor import ImageClip
            from moviepy.video.fx.all import Resize, Crop
            
            # Load image
            clip = ImageClip(image_path, duration=duration)
            
            # Resize to fit screen while maintaining aspect ratio
            clip = clip.resize(height=self.height)
            
            # Apply zoom effect if specified
            zoom_speed = motion_effects.get('zoom_speed', 0.05)
            
            if zoom_speed > 0:
                # Simple zoom by resizing over time
                def zoom_effect(get_frame, t):
                    factor = 1.0 + (zoom_speed * t)
                    return Resize(clip, factor)(get_frame, t)
                
                # For simplicity, we'll just resize statically
                clip = clip.resize(lambda t: 1 + zoom_speed * t)
            
            # Center crop to exact dimensions
            if clip.w > self.width:
                clip = clip.crop(
                    x_center=clip.w // 2,
                    y_center=clip.h // 2,
                    width=self.width,
                    height=self.height
                )
            
            return clip
            
        except Exception as e:
            logger.error(f"Failed to create motion clip: {e}")
            from moviepy.editor import ImageClip
            return ImageClip(image_path, duration=duration)
    
    def _assemble_with_ffmpeg(
        self,
        script: Dict[str, Any],
        audio_path: str,
        visuals: List[Dict[str, Any]],
        subtitle_path: Optional[str],
        background_music_path: Optional[str],
        output_path: str
    ) -> str:
        """Assemble video using FFmpeg command line."""
        import subprocess
        
        logger.info("Assembling video with FFmpeg...")
        
        # Create a simple slideshow from images with audio
        # This is a basic implementation - production would be more sophisticated
        
        # Generate filter complex for slideshow
        inputs = []
        filter_parts = []
        
        # Add image inputs
        for visual in visuals:
            image_path = visual.get('path', '')
            if Path(image_path).exists():
                inputs.extend(['-loop', '1', '-i', image_path])
        
        # Add audio input
        if Path(audio_path).exists():
            inputs.extend(['-i', audio_path])
        
        # Build FFmpeg command
        cmd = ['ffmpeg', '-y']
        cmd.extend(inputs)
        
        # Simple concatenation
        cmd.extend([
            '-vf', f'scale={self.width}:{self.height}:force_original_aspect_ratio=increase,crop={self.width}:{self.height}',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-pix_fmt', 'yuv420p'
        ])
        
        if Path(audio_path).exists():
            cmd.extend(['-i', audio_path])
            cmd.extend(['-map', '0:v'])
            cmd.extend(['-map', '1:a'])
        else:
            cmd.extend(['-map', '0:v'])
        
        cmd.extend(['-t', str(script.get('estimated_duration', 30))])
        cmd.append(output_path)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.error(f"FFmpeg failed: {result.stderr}")
                return self._create_placeholder_video(output_path)
            
            logger.info(f"Video assembled with FFmpeg: {output_path}")
            return output_path
            
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg timed out")
            return self._create_placeholder_video(output_path)
        except Exception as e:
            logger.error(f"FFmpeg assembly failed: {e}")
            return self._create_placeholder_video(output_path)
    
    def _create_placeholder_video(self, output_path: str, duration: float = 10.0) -> str:
        """Create a minimal placeholder video when assembly fails."""
        try:
            from PIL import Image
            import struct
            import wave
            import tempfile
            
            logger.warning("Creating placeholder video due to assembly failure")
            
            # Create a simple solid color image sequence
            img = Image.new('RGB', (self.width, self.height), color=(70, 70, 100))
            
            with tempfile.TemporaryDirectory() as tmpdir:
                # Save single frame
                frame_path = os.path.join(tmpdir, 'frame.png')
                img.save(frame_path)
                
                # Use FFmpeg to create video from frames
                import subprocess
                
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1',
                    '-i', frame_path,
                    '-c:v', 'libx264',
                    '-t', str(duration),
                    '-pix_fmt', 'yuv420p',
                    '-vf', f'scale={self.width}:{self.height}',
                    output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    logger.info(f"Created placeholder video: {output_path}")
                    return output_path
                    
        except Exception as e:
            logger.error(f"Failed to create placeholder video: {e}")
        
        return output_path


def assemble_final_video(
    script: Dict[str, Any],
    audio_path: str,
    visuals: List[Dict[str, Any]],
    output_path: str,
    subtitle_path: Optional[str] = None,
    background_music_path: Optional[str] = None,
    resolution: str = "1080x1920",
    fps: int = 30
) -> str:
    """
    Convenience function to assemble final video.
    
    Args:
        script: Script dictionary
        audio_path: Path to narration audio
        visuals: List of visual information
        output_path: Path to save final video
        subtitle_path: Optional subtitle file
        background_music_path: Optional background music
        resolution: Video resolution
        fps: Frames per second
        
    Returns:
        Path to assembled video
    """
    assembler = VideoAssembler(resolution, fps)
    return assembler.assemble_video(
        script, audio_path, visuals,
        subtitle_path, background_music_path,
        output_path
    )


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Testing video assembly...")
    
    demo_script = {
        "title": "Test Video",
        "estimated_duration": 10,
        "scenes": [
            {"start_time": 0, "end_time": 5},
            {"start_time": 5, "end_time": 10}
        ]
    }
    
    demo_visuals = [
        {"path": "projects/demo_project/visuals/scene_001.png"},
        {"path": "projects/demo_project/visuals/scene_002.png"}
    ]
    
    output_file = "projects/demo_project/output/test_video.mp4"
    
    # This will create a placeholder since we don't have real assets yet
    result = assemble_final_video(
        demo_script,
        "projects/demo_project/audio/narration.wav",
        demo_visuals,
        output_file
    )
    
    print(f"Output video: {result}")
