# src/actions/speak/connector/zenoh_speak.py
import logging
import time

import zenoh
from actions.base import ActionConfig, ActionConnector
from actions.speak.interface import SpeakInput


class ZenohSpeakConnector(ActionConnector[SpeakInput]):
    """A Zenoh-based speech connector that sends speech commands to the robot"""

    def __init__(self, config: ActionConfig):
        super().__init__(config)
        self.session = None

        # Get URID (robot ID)
        URID = getattr(self.config, "URID", None)
        if URID is None:
            logging.warning(f"Aborting speech, no URID provided")
            return
        else:
            logging.info(f"Speech system using URID: {URID}")

        # Define the speech topic
        self.speak_topic = f"{URID}/speak"
        
        # Initialize Zenoh session
        try:
            self.session = zenoh.open(zenoh.Config())
            logging.info("Zenoh client opened for speech")
        except Exception as e:
            logging.error(f"Error opening Zenoh client for speech: {e}")

    async def connect(self, output_interface: SpeakInput) -> None:
        """Called when the agent wants to speak"""
        if self.session is None:
            logging.info("No open Zenoh session for speech, returning")
            return
        
        # Get the text to speak
        text = output_interface.action
        
        # Log the speech action
        logging.info(f"Sending speech command: {text}")
        
        # Send the speech text over Zenoh
        self.session.put(self.speak_topic, text)

    def tick(self) -> None:
        """Called regularly by the agent system"""
        time.sleep(0.1)