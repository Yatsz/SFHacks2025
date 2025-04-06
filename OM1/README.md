
![OM_Banner_X2 (1)](https://github.com/user-attachments/assets/853153b7-351a-433d-9e1a-d257b781f93c)

<p align="center">  <a href="https://arxiv.org/abs/2412.18588">Technical Paper</a> |  <a href="https://docs.openmind.org/">Documentation</a> |  <a href="https://x.com/openmind_agi">X</a> | <a href="https://discord.gg/VUjpg4ef5n">Discord</a> </p>

**Openmind's OM1 is a modular AI runtime that empowers developers to create and deploy multimodal AI agents seamlessly across both digital environments and physical robots**, including Quadrupeds, TurtleBot 4 and Humanoids. OM1 agents can process diverse inputs like web data, social media, camera feeds, and LIDAR etc, while enabling physical interactions such as navigation, and natural conversations, effectively allowing users to interact with advanced AI models like GPT-4o in embodied form.

## Capabilities of OM1

* **Modular Architecture**: Designed with Python for simplicity and seamless integration.
* **Data Input**: Easily handles new data.
* **Hardware Support via Plugins**: Supports new hardware through plugins for API endpoints and specific robot hardware connections to `ROS2`, `Zenoh`, and `CycloneDDS`.
* **Web-Based Debugging Display**: Monitor the system in action with WebSim (available at http://localhost:8000/) for easy debugging through visuals.
* **Pre-configured Endpoints**: Supports Voice-to-Speech, OpenAI’s `gpt-4o`, DeepSeek, and multiple Visual Language Models (VLMs) with pre-configured endpoints for each service.

## Architecture Overview
  ![Artboard 1@4x 1 (1)](https://github.com/user-attachments/assets/14e9b916-4df7-4700-9336-2983c85be311)

## Quick Start

Let's run the first AI agent named Spot on OM1. The Spot agent uses your webcam to capture and label objects. These text captions are then sent to `OpenAI 4o`, a large language model (LLM) which then returns `movement`, `speech` and `face` action commands. These commands are displayed on WebSim along with basic timing and other debugging information.

1. Clone the repo.

```bash clone repo
git clone https://github.com/OpenmindAGI/OM1.git
cd OM1
git submodule update --init
```

2. Install Rust Python package manager `uv`

* On Mac, use `brew install uv`.
* On Linux, use `curl -LsSf https://astral.sh/uv/install.sh | sh`.

3. Install `portaudio`

* On Mac, use `brew install portaudio`
* On Linux, use `sudo apt-get install portaudio19-dev python-all-dev`

4. Set the configuration variables. 

Locate the `config` folder and add your Openmind API key in `/config/spot.json`. If you do not already have one, you can obtain a free access key at https://portal.openmind.org/.  _Note:_ Using the placeholder key **openmind-free** will generate errors.

```bash set api key
# /config/spot.json
...
"api_key": "om1_live_e4252f1cf005af..."
...
```

5. Run the `spot` agent.

```bash run spot
uv run src/run.py spot
```

6. WebSim to check input and output

Go to [http://localhost:8000](http://localhost:8000) to see real time logs along with the input and output in the terminal. For easy debugging, add `--debug` to see additional logging information.

**Congratulations!** - you just got started with OM1 and can now explore its capabilities.

## What's Next?

* Try out more tutorials, visit https://docs.openmind.org/examples/conversation
* Add new `inputs` and `actions`.
* Design custom agents and robots by creating your own json config file with different combinations of inputs and actions, based on your needs.
* Change the system prompts in the configuration files (located in `/config/`) to create new behaviors.

## Interfacing with New Robot Hardware

OM1 assumes that robot hardware provides a high-level SDK that accepts elemental movement and action commands such as `backflip`, `run`, `gently pick up the red apple`, `move(0.37, 0, 0)`, and `smile`. An example is provided in `actions/move_safe/connector/ros2.py`:

```
...
elif output_interface.action == "shake paw":
    if self.sport_client:
        self.sport_client.Hello()
...
```

If your robot hardware does not yet provide a suitable HAL (hardware abstraction layer), traditional robotics approaches such as RL (reinforcement learning) in concert with suitable simulation environments (Unity, Gazebo), sensors (such as hand mounted ZED depth cameras), and custom VLAs will be needed for you to create one. It is further assumed that your HAL accepts motion trajectories, provides all battery and thermal management/monitoring, and calibrates and tunes sensors such as IMUs, LIDARs, and magnetometers. OM1 can interface with your HAL via USB, serial, ROS2, CycloneDDS, Zenoh, or websockets. For an example of an advanced humanoid HAL, please see [Unitree's C++ SDK](https://github.com/unitreerobotics/unitree_sdk2/blob/adee312b081c656ecd0bb4e936eed96325546296/example/g1/high_level/g1_loco_client_example.cpp#L159). Frequently, a HAL, especially ROS2 code, will be dockerized and can then interface with OM1 through DDS middleware or websockets.   

## Recommended Development Platforms

OM1 is developed on:

* Jetson AGX Orin 64GB (running Ubuntu 22.04 and JetPack 6.1)
* Mac Studio with Apple M2 Ultra with 48 GB unified memory (running macOS Sequoia)
* Mac Mini with Apple M4 Pro with 48 GB unified memory (running macOS Sequoia)
* Generic Linux machines (running Ubuntu 22.04)

OM1 _should_ run on other platforms (such as Windows) and microcontrollers such as the Raspberry Pi 5 16GB.

## Detailed Documentation

More detailed documentation can be accessed at [docs.openmind.org](https://docs.openmind.org/).

## Contributing

Please make sure to read the [Contributing Guide](./CONTRIBUTING.md) before making a pull request.

## License

This project is licensed under the terms of the MIT License, which is a permissive free software license that allows users to freely use, modify, and distribute the software. The MIT License is a widely used and well-established license that is known for its simplicity and flexibility. By using the MIT License, this project aims to encourage collaboration, modification, and distribution of the software.
