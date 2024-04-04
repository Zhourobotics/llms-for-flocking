<div align="center">
  <h1>Challenges Faced by Large Language Models in<br>Solving Multi-Agent Flocking</h1>
</div>

This repository contains our implementation of our papers flocking simulation.


https://github.com/Zhourobotics/llms-for-flocking/assets/55445872/7c6c584d-1350-48a3-94b4-f36e4e074728


## Prerequisites

- Make sure you have [Python](https://www.python.org/downloads/) installed
- This project has a few dependencies, install them with `pip install -r requirements.txt`
- You'll also need one or more valid OpenAI API keys. When you have them in hand, create a file titled `secrets.yml` and add them in the following format:
    ```yml
    api_keys:
        0: "sk-YourFirstAPIKeyHere"
        1: "sk-YourSecondAPIKeyHere"
        2: "sk-YourThirdAPIKeyHere"
    ```

## Usage
```
usage: main.py --mode {run, plot} --name TEST_NAME
               [--agents AMOUNT_OF_AGENTS] [--rounds AMOUNT_OF_ROUNDS]
               [--seed RANDOM_SEED] 
               [--prompt PROMPT]
               [--round_description ROUND_DESCRIPTION]
               [--spawn_x_min SPAWN_X_MIN] [--spawn_x_max SPAWN_X_MAX]
               [--spawn_y_min SPAWN_Y_MIN] [--spawn_y_max SPAWN_Y_MAX]
               [--model GPT_MODEL] [--memory_limit MEMORY_LIMIT]
               [--x_min X_MIN] [--x_max X_MAX] [--x_ticks X_TICKS]
               [--y_min Y_MIN] [--y_max Y_MAX]
```

## Example
```
example: main.py --mode run --name mytest 
                 -a 3 -t 15
                 -s 42
                 -p "Your position is: [{}]. There are other drones in this space and their positions (in the format [[x, y], [x, y]...]) are: [{}]. Your task is to collectively implement a flocking behavior. Attempt to match the velocity of nearby agents and adjust your movement to align with this average direction. If you are not near any other agents, move towards the center of mass of nearby agents to stay close to the group. Calculate the distance between yourself and other agents. If any agent is closer than 4 units, you MUST move away to maintain personal space. It is critical you maintain a distance between drones. If you are close to any other drones you MUST move away, otherwise you fail the task."
                 -r "Your position is: [{}]. The positions of the other drones (in the format [[x, y], [x, y]...]) are: [{}]. Pick a position to move to, and briefly explain the reasoning behind your decision."
                 --x_min -10 --x_max 30 --x_ticks 5 --y_min 0 --y_max 20
```
