import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import json5

from actions import load_action
from actions.base import AgentAction
from inputs import load_input
from inputs.base import Sensor, SensorConfig
from llm import LLM, LLMConfig, load_llm
from llm.output_model import CortexOutputModel
from runtime.robotics import load_unitree
from simulators import load_simulator
from simulators.base import Simulator, SimulatorConfig


@dataclass
class RuntimeConfig:
    """Runtime configuration for the agent."""

    hertz: float
    name: str
    system_prompt_base: str
    system_governance: str
    system_prompt_examples: str
    agent_inputs: List[Sensor]
    cortex_llm: LLM
    simulators: List[Simulator]
    agent_actions: List[AgentAction]

    # Optional API key for the runtime configuration
    api_key: Optional[str] = None

    # Optional URID robot id key for the runtime configuration
    URID: Optional[str] = None

    # Optional Ethernet adapter setting for Unitree Robots
    unitree_ethernet: Optional[str] = None

    @classmethod
    def load(cls, config_name: str) -> "RuntimeConfig":
        """Load a runtime configuration from a file."""
        return load_config(config_name)


def load_config(config_name: str) -> RuntimeConfig:
    """
    Load and parse a runtime configuration from a JSON file.

    Parameters
    ----------
    config_name : str
        Name of the configuration file (without .json extension)

    Returns
    -------
    RuntimeConfig
        Parsed runtime configuration object

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist
    json.JSONDecodeError
        If the configuration file contains invalid JSON
    KeyError
        If required configuration fields are missing
    ImportError
        If component types specified in config cannot be imported
    ValueError
        If configuration values are invalid (e.g., negative hertz)
    """
    config_path = os.path.join(
        os.path.dirname(__file__), "../../config", config_name + ".json5"
    )

    with open(config_path, "r+") as f:
        raw_config = json5.load(f)

    g_api_key = raw_config.get("api_key", None)
    if g_api_key is None or g_api_key == "":
        logging.warning(
            "No API key found in the configuration file. Rate limits may apply."
        )

    if g_api_key == "openmind_free":
        logging.info("Checking for backup OM_API_KEY in your .env file.")
        backup_key = os.environ.get("OM_API_KEY")
        if backup_key:
            g_api_key = backup_key
            logging.info("Success - Found OM_API_KEY in your .env file.")
        else:
            logging.warning(
                "Could not find backup OM_API_KEY in your .env file. Using 'openmind_free'. Rate limits will apply."
            )

    g_URID = raw_config.get("URID", None)
    if g_URID is None or g_URID == "":
        logging.warning(
            "No URID found in the configuration file. Multirobot deployments will conflict."
        )

    if g_URID == "default":
        logging.info("Checking for backup URID in your .env file.")
        backup_URID = os.environ.get("URID")
        if backup_URID:
            g_URID = backup_URID
            logging.info("Success - Found URID in your .env file.")
        else:
            logging.warning(
                "Could not find backup URID in your .env file. Using 'default'. Multirobot deployments will conflict."
            )

    g_ut_eth = raw_config.get("unitree_ethernet", None)
    if g_ut_eth is None or g_ut_eth == "":
        logging.info("No robot hardware ethernet port provided.")
    else:
        # Load Unitree robot communication channel, if needed
        load_unitree(g_ut_eth)

    conf = raw_config["cortex_llm"].get("config", {})
    logging.debug(f"config {conf}")

    parsed_config = {
        **raw_config,
        "agent_inputs": [
            load_input(input["type"])(
                config=SensorConfig(
                    **add_meta(input.get("config", {}), g_api_key, g_ut_eth, g_URID)
                )
            )
            for input in raw_config.get("agent_inputs", [])
        ],
        "cortex_llm": load_llm(raw_config["cortex_llm"]["type"])(
            config=LLMConfig(
                **add_meta(
                    raw_config["cortex_llm"].get("config", {}),
                    g_api_key,
                    g_ut_eth,
                    g_URID,
                )
            ),
            output_model=CortexOutputModel,
        ),
        "simulators": [
            load_simulator(simulator["type"])(
                config=SimulatorConfig(
                    name=simulator["type"],
                    **add_meta(
                        simulator.get("config", {}), g_api_key, g_ut_eth, g_URID
                    ),
                )
            )
            for simulator in raw_config.get("simulators", [])
        ],
        "agent_actions": [
            load_action(
                {
                    **action,
                    "config": add_meta(
                        action.get("config", {}), g_api_key, g_ut_eth, g_URID
                    ),
                }
            )
            for action in raw_config.get("agent_actions", [])
        ],
    }

    return RuntimeConfig(**parsed_config)


def add_meta(
    config: Dict,
    g_api_key: Optional[str],
    g_ut_eth: Optional[str],
    g_URID: Optional[str],
) -> dict:
    """
    Add an API key and Robot configuration to a runtime configuration.

    Parameters
    ----------
    config : dict
        The runtime configuration to update.
    g_api_key : str
        The API key to add.
    g_ut_eth : str
        The Robot ethernet port to add.
    g_URID : str
        The Robot URID to use.

    Returns
    -------
    dict
        The updated runtime configuration.
    """

    # logging.info(f"config before {config}")
    if "api_key" not in config and g_api_key is not None:
        config["api_key"] = g_api_key
    if "unitree_ethernet" not in config and g_ut_eth is not None:
        config["unitree_ethernet"] = g_ut_eth
    if "URID" not in config and g_URID is not None:
        config["URID"] = g_URID
    # logging.info(f"config after {config}")
    return config
