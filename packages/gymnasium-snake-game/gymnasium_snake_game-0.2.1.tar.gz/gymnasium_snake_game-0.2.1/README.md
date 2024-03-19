# Snake game for Farama Gymnasium

This project is based on [Snake game for OpenAI Gym](https://github.com/NaLooo/Gym_Snake_Game) by Ming Yu.

Additional changes include:
 - changing observations to 2D image data
 - fixing display settings code
 - changing default parameters, including rewards, board size, and colors palette

# Snake game for OpenAI Gym
![Python versions](https://img.shields.io/pypi/pyversions/gym-snake-game)
[![PyPI](https://img.shields.io/pypi/v/gym-snake-game)](https://pypi.org/project/gym-snake-game/)
[![License](https://img.shields.io/github/license/NaLooo/Gym_Snake_Game)](https://github.com/NaLooo/Gym_Snake_Game/blob/main/LICENSE)

![screenshot](/resource/screenshot.png)

## Quick Start
```python
import gym_snake_game
import gymnasium

# both work
env = gymnasium.make('Snake-v0', render_mode='human')
env = gym_snake_game.make('Snake-v0', render_mode='human')
env.reset()

# for human playing
env.play()

# for ai playing
while True:
    obs, reward, done, truncated, info = env.step(env.action_space.sample())
    if done:
        break
env.close()

```
## Available Options
```python
import gym_snake_game

options = {
    'fps': 60,
    'max_step': 500,
    'init_length': 4,
    'food_reward': 2.0,
    'dist_reward': None,
    'living_bonus': 0.0,
    'death_penalty': -1.0,
    'width': 40,
    'height': 40,
    'block_size': 20,
    'background_color': (255, 169, 89),
    'food_color': (255, 90, 90),
    'head_color': (197, 90, 255),
    'body_color': (89, 172, 255),
}

env = gym_snake_game.make('Snake-v0', render_mode='human', **options)

```

## Requirements

-   Python >= 3.0
-   Numpy >= 1.23.2
-   Pygame >= 2.1.3
-   Gymnasium >= 0.29.0
