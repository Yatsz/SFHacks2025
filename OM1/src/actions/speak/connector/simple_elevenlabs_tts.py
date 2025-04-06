import asyncio
import base64
import io
import logging
import os
import requests
from pydub import AudioSegment
from pydub.playback import play

from actions.base import ActionConfig, ActionConnector
from actions.speak.interface import SpeakInput


class SimpleElevenLabsTTSConnector(ActionConnector[SpeakInput]):
    """A simplified ElevenLabs TTS connector that directly plays audio"""

    def __init__(self, config: ActionConfig):
        super().__init__(config)
        
        # Get configuration values from global config
        self.api_key = getattr(config, "api_key", None)
        self.voice_id = getattr(config, "voice_id", "i4CzbCVWoqvD0P1QJCUL")
        self.model_id = getattr(config, "model_id", "eleven_monolingual_v1")
        self.speaker_device_id = getattr(config, "speaker_device_id", 1)  # Default to USB speaker
        
        # OpenMind API endpoint
        self.api_url = "https://api.openmind.org/api/core/elevenlabs/tts"
        
        # Log configuration
        logging.info(f"Initialized SimpleElevenLabsTTSConnector with voice: {self.voice_id}")
        logging.info(f"Using speaker device ID: {self.speaker_device_id}")

    async def connect(self, output_interface: SpeakInput) -> None:
        # Get the text to speak
        text = output_interface.action
        
        logging.info(f"Speaking: '{text}'")
        
        # Request TTS and play audio
        try:
            audio_data = await self._tts_request(text)
            if audio_data:
                success = await self._play_audio(audio_data)
                if not success:
                    logging.error("Failed to play audio")
            else:
                logging.error("Failed to get audio data from API")
        except Exception as e:
            logging.error(f"Error in TTS process: {e}")

    async def _tts_request(self, text):
        """Request TTS from ElevenLabs via OpenMind API"""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "text": text,
            "voice_id": self.voice_id,
            "model_id": self.model_id
        }
        
        logging.info(f"Requesting TTS for: '{text}'")
        
        # Run the request in a thread pool to avoid blocking
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.post(self.api_url, json=data, headers=headers)
        )
        
        if response.status_code != 200:
            logging.error(f"API Error: {response.status_code}")
            logging.error(response.text)
            return None
        
        try:
            json_response = response.json()
            if 'response' not in json_response:
                logging.error("No audio data in response")
                return None
            
            # Decode base64 to binary
            audio_data = base64.b64decode(json_response['response'])
            return audio_data
        except Exception as e:
            logging.error(f"Error processing API response: {e}")
            return None

    async def _play_audio(self, audio_data):
        """Play audio data through the USB speaker"""
        # Set up audio device
        os.system(f"pactl set-default-sink {self.speaker_device_id}")
        os.system(f"pactl set-sink-mute {self.speaker_device_id} 0")
        os.system(f"pactl set-sink-volume {self.speaker_device_id} 100%")
        
        # Try multiple playback methods
        
        # 1. Try pydub first
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self._play_with_pydub(audio_data)
            )
            return True
        except Exception as e:
            logging.error(f"pydub playback failed: {e}")
        
        # 2. Fall back to mpg123
        try:
            import tempfile
            import subprocess
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(audio_data)
            
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: subprocess.run(["mpg123", temp_filename], check=True)
            )
            
            # Clean up
            os.unlink(temp_filename)
            return True
        except Exception as e:
            logging.error(f"mpg123 playback failed: {e}")
            return False
    
    def _play_with_pydub(self, audio_data):
        """Helper method to play audio with pydub"""
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        play(audio)