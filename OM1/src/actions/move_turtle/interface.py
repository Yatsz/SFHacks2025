from dataclasses import dataclass
from enum import Enum

from actions.base import Interface


class MovementAction(str, Enum):
    TURN_LEFT = "turn left"
    TURN_RIGHT = "turn right"
    MOVE_FORWARDS = "move forwards"
    MOVE_BACK = "move back"
    AVOID_LEFT_OBSTRACLE = "avoid left obstacle"
    AVOID_RIGHT_OBSTRACLE = "avoid right obstacle"
    STAND_STILL = "stand still"


@dataclass
class MoveInput:
    action: MovementAction


@dataclass
class Move(Interface[MoveInput, MoveInput]):
    """
    A movement to be performed by the agent.
    Effect: Allows the agent to move.
    """

    input: MoveInput
    output: MoveInput
