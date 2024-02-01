# LLMS For Flocking
The first ever flocking LLM paper!

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
               [--rounds AMOUNT_OF_ROUNDS] [--agents AMOUNT_OF_AGENTS]
               [--seed RANDOM_SEED]
               [--spawn_x_min SPAWN_X_MIN] [--spawn_x_max SPAWN_X_MAX]
               [--spawn_y_min SPAWN_Y_MIN] [--spawn_y_max SPAWN_Y_MAX]
               [--shape FLOCK_SHAPE] [--max_velocity MAX_AGENT_VELOCITY]
               [--safe_distance SAFE_DISTANCE_BETWEEN_AGENTS]
               [--model GPT_MODEL] [--memory_limit MEMORY_LIMIT]
               [--x_min X_MIN] [--x_max X_MAX] [--x_ticks X_TICKS]
               [--y_min Y_MIN] [--y_max Y_MAX]
```