"""
Voice/TTS processor for generating narration audio.
Supports multiple free TTS engines: edge-tts, piper, coqui.
"""

import asyncio
import os
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Generate voiceover audio from text using free TTS engines."""
    
    def __init__(self, engine: str = "edge-tts", voice: str = "en-US-JennyNeural"):
        """
        Initialize voice processor.
        
        Args:
            engine: TTS engine (edge-tts, piper, coqui)
            voice: Voice identifier for the selected engine
        """
        self.engine = engine.lower()
        self.voice = voice
        self.output_format = "wav"
    
    def generate_audio(
        self,
        text: str,
        output_path: str,
        speed: float = 1.0,
        pitch: int = 0,
        volume: int = 100
    ) -> str:
        """
        Generate audio from text.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            speed: Speech speed multiplier
            pitch: Pitch adjustment
            volume: Volume percentage
            
        Returns:
            Path to generated audio file
        """
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.engine == "edge-tts":
            return self._generate_edge_tts(text, str(path), speed, pitch, volume)
        elif self.engine == "piper":
            return self._generate_piper(text, str(path), speed)
        elif self.engine == "coqui":
            return self._generate_coqui(text, str(path), speed)
        else:
            logger.warning(f"Unknown TTS engine '{self.engine}'. Using edge-tts fallback.")
            return self._generate_edge_tts(text, str(path), speed, pitch, volume)
    
    def _generate_edge_tts(
        self,
        text: str,
        output_path: str,
        speed: float = 1.0,
        pitch: int = 0,
        volume: int = 100
    ) -> str:
        """Generate audio using edge-tts (Microsoft's free neural TTS)."""
        try:
            import edge_tts
            
            # Adjust rate based on speed
            rate = f"{int((speed - 1.0) * 100):+d}%"
            pitch_str = f"{pitch:+d}Hz"
            volume_str = f"{volume:+d}%"
            
            # Run edge-tts asynchronously
            asyncio.run(
                self._run_edge_tts(text, output_path, self.voice, rate, pitch_str, volume_str)
            )
            
            logger.info(f"Generated audio with edge-tts: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("edge-tts not installed. Install with: pip install edge-tts")
            return self._create_silence_fallback(output_path)
        except Exception as e:
            logger.error(f"edge-tts generation failed: {e}")
            return self._create_silence_fallback(output_path)
    
    async def _run_edge_tts(self, text, output_path, voice, rate, pitch, volume):
        """Run edge-tts synthesis."""
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
        await communicate.save(output_path)
    
    def _generate_piper(
        self,
        text: str,
        output_path: str,
        speed: float = 1.0
    ) -> str:
        """Generate audio using Piper TTS (local, fast)."""
        try:
            # Piper requires command-line execution
            # This is a placeholder - actual implementation depends on Piper installation
            piper_cmd = f'echo "{text}" | piper --model en_US-lessac-medium --output_file "{output_path}"'
            
            # Note: This requires Piper to be installed separately
            # For demo purposes, we'll create a fallback
            logger.warning("Piper TTS requires separate installation. Using fallback.")
            return self._create_silence_fallback(output_path)
            
        except Exception as e:
            logger.error(f"Piper generation failed: {e}")
            return self._create_silence_fallback(output_path)
    
    def _generate_coqui(
        self,
        text: str,
        output_path: str,
        speed: float = 1.0
    ) -> str:
        """Generate audio using Coqui TTS (open-source)."""
        try:
            from TTS.api import TTS
            
            # Initialize TTS (first run will download model)
            tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
            
            # Generate speech
            tts.tts_to_file(text=text, file_path=output_path)
            
            logger.info(f"Generated audio with Coqui TTS: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("Coqui TTS not installed. Install with: pip install TTS")
            return self._create_silence_fallback(output_path)
        except Exception as e:
            logger.error(f"Coqui TTS generation failed: {e}")
            return self._create_silence_fallback(output_path)
    
    def _create_silence_fallback(self, output_path: str, duration: float = 5.0) -> str:
        """
        Create a silent audio file as fallback.
        
        Args:
            output_path: Path to save silent audio
            duration: Duration in seconds
            
        Returns:
            Path to created file
        """
        try:
            # Create minimal WAV file header for silence
            # This is a simple mono silent WAV
            import wave
            import struct
            
            sample_rate = 44100
            duration_samples = int(sample_rate * duration)
            
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Write silence (zeros)
                for _ in range(duration_samples):
                    wav_file.writeframes(struct.pack('h', 0))
            
            logger.warning(f"Created silent audio fallback: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create silence fallback: {e}")
            return output_path
    
    def list_available_voices(self) -> list:
        """List available voices for the current engine."""
        if self.engine == "edge-tts":
            return self._list_edge_tts_voices()
        else:
            return [self.voice]
    
    def _list_edge_tts_voices(self) -> list:
        """List available edge-tts voices."""
        try:
            import edge_tts
            voices = asyncio.run(edge_tts.list_voices())
            return [v['ShortName'] for v in voices]
        except Exception as e:
            logger.error(f"Failed to list voices: {e}")
            return ["en-US-JennyNeural", "en-US-GuyNeural", "en-US-AriaNeural"]


def generate_voiceover(
    text: str,
    output_path: str,
    engine: str = "edge-tts",
    voice: str = "en-US-JennyNeural",
    speed: float = 1.0,
    pitch: int = 0
) -> str:
    """
    Convenience function to generate voiceover.
    
    Args:
        text: Text to convert to speech
        output_path: Path to save audio
        engine: TTS engine
        voice: Voice identifier
        speed: Speech speed
        pitch: Pitch adjustment
        
    Returns:
        Path to generated audio
    """
    processor = VoiceProcessor(engine, voice)
    return processor.generate_audio(text, output_path, speed, pitch)


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    print("Testing voice generation...")
    test_text = "This is a test of the faceless viral video bot voice generation system."
    
    output_file = "projects/demo_project/audio/test_narration.wav"
    result = generate_voiceover(test_text, output_file)
    
    print(f"Audio generated: {result}")
    print(f"File exists: {Path(result).exists()}")
