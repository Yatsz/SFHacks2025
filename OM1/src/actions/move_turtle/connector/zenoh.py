import logging
import time
from dataclasses import dataclass

import zenoh
from pycdr2 import IdlStruct
from pycdr2.types import float64

from actions.base import ActionConfig, ActionConnector
from actions.move_turtle.interface import MoveInput


@dataclass
class Vector3(IdlStruct, typename="Vector3"):
    x: float64
    y: float64
    z: float64


@dataclass
class Twist(IdlStruct, typename="Twist"):
    linear: Vector3
    angular: Vector3


class MoveZenohConnector(ActionConnector[MoveInput]):

    def __init__(self, config: ActionConfig):
        super().__init__(config)
        self.session = None
        self.is_command_executing = False
        self.command_execution_time = 0
        self.command_timeout = 2.0

        URID = getattr(self.config, "URID", None)

        if URID is None:
            # Log the domain id being used
            logging.warning(f"Aborting Move, no URID provided: {URID}")
            return
        else:
            logging.warning(f"Move system is using URID:{URID}")

        self.cmd_vel = f"{URID}/c3/cmd_vel"
        try:
            self.session = zenoh.open(zenoh.Config())
            logging.info("Zenoh client opened")
        except Exception as e:
            logging.error(f"Error opening Zenoh client: {e}")

    def pub_twist(self, linear, angular):
        if self.session is None:
            logging.info("No open Zenoh session, returning")
            return
        logging.info("Pub twist: {} - {}".format(linear, angular))
        t = Twist(
            linear=Vector3(x=float(linear), y=0.0, z=0.0),
            angular=Vector3(x=0.0, y=0.0, z=float(angular)),
        )
        self.session.put(self.cmd_vel, t.serialize())

        if linear != 0.0 or angular != 0.0:
            self.is_command_executing = True
            self.command_execution_time = time.time()
        else:
            self.is_command_executing = False

    async def connect(self, output_interface: MoveInput) -> None:
        if self.is_command_executing:
            current_time = time.time()
            elapsed_time = current_time - self.command_execution_time

            if elapsed_time < self.command_timeout:
                logging.debug(
                    f"Discarding command: {output_interface.action} - previous command still executing"
                )
                return
            else:
                logging.debug(
                    f"Previous command timed out, executing new command: {output_interface.action}"
                )
                self.is_command_executing = False

        logging.info(f"SendThisToZenoh: {output_interface.action}")

        if output_interface.action == "turn left":
            logging.info(f"Zenoh command: {output_interface.action}")
            self.pub_twist(0.3, 0.3)
        elif output_interface.action == "turn right":
            logging.info(f"Zenoh command: {output_interface.action}")
            self.pub_twist(0.3, -0.3)
        elif output_interface.action == "move forwards":
            logging.info(f"Zenoh command: {output_interface.action}")
            self.pub_twist(0.5, 0.0)
        elif output_interface.action == "move back":
            logging.info(f"Zenoh command: {output_interface.action}")
            self.pub_twist(-0.5, 0.0)
        elif output_interface.action == "spin around":
            logging.info(f"Zenoh command: {output_interface.action}")
            self.pub_twist(0.0, 0.8)
        elif output_interface.action == "stand still":
            logging.info(f"Zenoh command: {output_interface.action}")
            # do nothing
        else:
            logging.info(f"Unknown move type: {output_interface.action}")

    def tick(self) -> None:

        time.sleep(0.1)
