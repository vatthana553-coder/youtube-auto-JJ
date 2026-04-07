"""
Main entry point for Faceless Viral Video Bot.
Provides CLI interface for the complete video generation pipeline.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config_manager import get_config, Config
from utils.logger import setup_logging, get_logger
from generators.topic_generator import TopicGenerator, generate_topics
from generators.script_writer import ScriptWriter, write_script
from processors.voice_processor import VoiceProcessor, generate_voiceover
from processors.subtitle_processor import SubtitleProcessor, generate_subtitles
from processors.visual_processor import VisualProcessor, generate_visuals
from assemblers.video_assembler import VideoAssembler, assemble_final_video
from generators.metadata_generator import MetadataGenerator, generate_video_metadata


logger = logging.getLogger(__name__)


class VideoPipeline:
    """Complete video generation pipeline."""
    
    def __init__(self, config: Config):
        """Initialize pipeline with configuration."""
        self.config = config
        self.project_name = ""
        self.project_paths = {}
    
    def run_full_pipeline(
        self,
        niche: str = None,
        topic: str = None,
        duration: int = None,
        tone: str = None,
        voice: str = None,
        output_dir: str = None
    ) -> dict:
        """
        Run complete video generation pipeline.
        
        Args:
            niche: Content niche
            topic: Specific topic (optional - will be generated if not provided)
            duration: Video duration in seconds
            tone: Script tone
            voice: TTS voice
            output_dir: Output directory
            
        Returns:
            Dictionary with pipeline results
        """
        # Get configuration values
        niche = niche or self.config.get('niche.default', 'science')
        duration = duration or self.config.get('general.duration', 45)
        tone = tone or self.config.get('niche.tone', 'curious')
        voice = voice or self.config.get('tts.voice', 'en-US-JennyNeural')
        
        # Generate project name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.project_name = f"video_{niche}_{timestamp}"
        
        if output_dir:
            base_output = Path(output_dir)
        else:
            base_output = Path(self.config.get('paths.projects_root', 'projects'))
        
        self.project_paths = self.config.ensure_project_dirs(self.project_name)
        output_path = base_output / self.project_name
        
        logger.info(f"Starting video generation pipeline")
        logger.info(f"Niche: {niche}, Duration: {duration}s, Tone: {tone}")
        
        results = {
            "project_name": self.project_name,
            "project_path": str(output_path),
            "steps": {}
        }
        
        try:
            # Step 1: Generate topic ideas
            logger.info("Step 1: Generating topic ideas...")
            topic_result = generate_topics(niche, count=5, output_dir=str(output_path / "script"))
            results["steps"]["topics"] = topic_result
            
            # Select best topic if none provided
            if not topic and topic_result.get('best_idea'):
                topic = topic_result['best_idea']['title']
                logger.info(f"Selected topic: {topic}")
            
            # Step 2: Write script
            logger.info("Step 2: Writing script...")
            script = write_script(
                topic=topic or f"Amazing {niche.title()} Facts",
                niche=niche,
                duration=duration,
                tone=tone,
                output_dir=str(output_path / "script")
            )
            results["steps"]["script"] = script
            
            # Step 3: Generate voiceover
            logger.info("Step 3: Generating voiceover...")
            tts_engine = self.config.get('tts.engine', 'edge-tts')
            audio_path = str(output_path / "audio" / "narration.wav")
            
            voiceover_path = generate_voiceover(
                text=script['narration'],
                output_path=audio_path,
                engine=tts_engine,
                voice=voice,
                speed=self.config.get('tts.speed', 1.0),
                pitch=self.config.get('tts.pitch', 0)
            )
            results["steps"]["audio"] = {"path": voiceover_path}
            
            # Step 4: Generate subtitles
            logger.info("Step 4: Generating subtitles...")
            subtitle_style = self.config.get('subtitles.style', 'modern')
            subtitle_results = generate_subtitles(
                scenes=script['scenes'],
                output_dir=str(output_path / "subtitles"),
                style=subtitle_style
            )
            results["steps"]["subtitles"] = subtitle_results
            
            # Step 5: Generate visuals
            logger.info("Step 5: Generating visuals...")
            visual_style = self.config.get('visuals.style', 'mixed')
            visuals = generate_visuals(
                scenes=script['scenes'],
                output_dir=str(output_path / "visuals"),
                topic=topic,
                style=visual_style
            )
            results["steps"]["visuals"] = visuals
            
            # Step 6: Assemble video
            logger.info("Step 6: Assembling video...")
            resolution = self.config.get('general.resolution', '1080x1920')
            fps = self.config.get('general.fps', 30)
            
            video_path = str(output_path / "output" / "final_video.mp4")
            
            final_video = assemble_final_video(
                script=script,
                audio_path=voiceover_path,
                visuals=visuals,
                output_path=video_path,
                subtitle_path=subtitle_results.get('srt'),
                background_music_path=None,  # Can add later
                resolution=resolution,
                fps=fps
            )
            results["steps"]["video"] = {"path": final_video}
            
            # Step 7: Generate metadata
            logger.info("Step 7: Generating metadata...")
            platform = self.config.get('metadata.platform', 'youtube')
            metadata = generate_video_metadata(
                script=script,
                output_dir=str(output_path / "metadata"),
                platform=platform
            )
            results["steps"]["metadata"] = metadata
            
            logger.info(f"Pipeline completed successfully!")
            logger.info(f"Final video: {final_video}")
            
            results["success"] = True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            results["success"] = False
            results["error"] = str(e)
        
        return results
    
    def run_demo(self) -> dict:
        """Run demo pipeline with sample content."""
        logger.info("Running demo pipeline...")
        
        return self.run_full_pipeline(
            niche="science",
            topic="Black Holes",
            duration=30,
            tone="dramatic",
            output_dir="projects"
        )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Faceless Viral Video Bot - AI-powered short-form video generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --niche science --duration 45
  %(prog)s --demo
  %(prog)s --interactive
  %(prog)s --niche history --topic "Ancient Rome" --tone dramatic
        """
    )
    
    parser.add_argument('--niche', '-n', type=str, default=None,
                       help='Content niche (facts, history, science, mysteries, finance, what_if)')
    parser.add_argument('--topic', '-t', type=str, default=None,
                       help='Specific topic title')
    parser.add_argument('--duration', '-d', type=int, default=None,
                       help='Video duration in seconds (20-60 recommended)')
    parser.add_argument('--tone', type=str, default=None,
                       help='Script tone (curious, dramatic, educational, mysterious)')
    parser.add_argument('--voice', '-v', type=str, default=None,
                       help='TTS voice identifier')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output directory')
    parser.add_argument('--config', '-c', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--demo', action='store_true',
                       help='Run demo pipeline')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level=log_level)
    
    # Load configuration
    config = get_config(args.config)
    
    # Create pipeline
    pipeline = VideoPipeline(config)
    
    try:
        if args.demo:
            # Run demo
            results = pipeline.run_demo()
        elif args.interactive:
            # Interactive mode
            results = run_interactive(pipeline, config)
        else:
            # Standard mode
            results = pipeline.run_full_pipeline(
                niche=args.niche,
                topic=args.topic,
                duration=args.duration,
                tone=args.tone,
                voice=args.voice,
                output_dir=args.output
            )
        
        # Print results
        print("\n" + "=" * 60)
        print("PIPELINE RESULTS")
        print("=" * 60)
        print(f"Project: {results.get('project_name', 'Unknown')}")
        print(f"Status: {'✓ SUCCESS' if results.get('success') else '✗ FAILED'}")
        print(f"Output: {results.get('project_path', 'Unknown')}")
        
        if results.get('success'):
            print("\nGenerated files:")
            steps = results.get('steps', {})
            if 'video' in steps:
                print(f"  📹 Video: {steps['video'].get('path', 'N/A')}")
            if 'script' in steps:
                print(f"  📝 Script: {steps['script'].get('title', 'N/A')}")
            if 'audio' in steps:
                print(f"  🎵 Audio: {steps['audio'].get('path', 'N/A')}")
            if 'metadata' in steps:
                print(f"  🏷️  Metadata: Generated")
        
        print("=" * 60)
        
        # Exit with appropriate code
        sys.exit(0 if results.get('success') else 1)
        
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


def run_interactive(pipeline: VideoPipeline, config: Config) -> dict:
    """Run pipeline in interactive mode."""
    print("\n" + "=" * 60)
    print("FACELESS VIRAL VIDEO BOT - Interactive Mode")
    print("=" * 60)
    
    # Get available niches
    available_niches = config.get('niche.available', 
                                  ['facts', 'history', 'science', 'mysteries', 'finance', 'what_if'])
    
    print(f"\nAvailable niches: {', '.join(available_niches)}")
    
    # Prompt for inputs
    niche = input(f"\nSelect niche [{config.get('niche.default', 'science')}]: ").strip()
    if not niche:
        niche = config.get('niche.default', 'science')
    
    topic = input("Enter topic title (leave empty to auto-generate): ").strip()
    if not topic:
        topic = None
    
    duration_str = input(f"Duration in seconds [{config.get('general.duration', 45)}]: ").strip()
    duration = int(duration_str) if duration_str else config.get('general.duration', 45)
    
    tone = input(f"Tone [{config.get('niche.tone', 'curious')}]: ").strip()
    if not tone:
        tone = config.get('niche.tone', 'curious')
    
    print(f"\nStarting pipeline with:")
    print(f"  Niche: {niche}")
    print(f"  Topic: {topic or '(auto-generated)'}")
    print(f"  Duration: {duration}s")
    print(f"  Tone: {tone}")
    
    confirm = input("\nProceed? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return {"success": False, "error": "User cancelled"}
    
    return pipeline.run_full_pipeline(
        niche=niche,
        topic=topic,
        duration=duration,
        tone=tone
    )


if __name__ == "__main__":
    main()
