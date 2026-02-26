# Cerberus 

```
_________             ___.                              
\_   ___ \  __________\_ |__   ___________ __ __  ______
/    \  \/_/ __ \_  __ \ __ \_/ __ \_  __ \  |  \/  ___/
\     \___\  ___/|  | \/ \_\ \  ___/|  | \/  |  /\___ \ 
  \______  /\___  >__|  |___  /\___  >__|  |____//____ >
```

## ℹ️ Overview

[Cerberus-bot](https://lichess.org/@/Cerberus_bot) is a homemade chess engine that can play at ~1800 ELO. It is live on Lichess so you can play against it using this [Link](https://lichess.org/@/Cerberus_bot)

Cerberus-bot is a chess engine built with Python with python-chess library using PyPy, just in time compilation for maximum performance.
It follows the classical chess engine design pattern, with minimax search, alpha-beta pruning, iterative deepening, and transposition table. 

Chess engine is usually built with C or C++ for their performance and efficiency. However, I found python to be a great language to get started with chess engine development due to its simplicity and readability at the cost of performance.

### Authors

Check out my [github](https://github.com/hiimstevejin) 

## Usage

At this stage, you can play against it. But I will integrate it with my own front & backend so that it can be played independently in my website 

## Architecture

In a virtual machine this project runs with [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) and communicates with Lichess through the [UCI protocol](https://en.wikipedia.org/wiki/Universal_Chess_Interface). 

The reason why this code is decoupled is because intense computation is required for chess engine and could crash the backend server if deployed on a shared hosting environment. 

## Installation

1. clone this repo
```
git clone https://github.com/hiimstevejin/Cerberus-Chess-Engine.git
cd Cerberus-Chess-Engine
```

2. Install Dependencies and run to see uci protocol in terminal
```
uv sync
uv run python main.py
```

## Reference
This was the main resource I looked at to get started with chess engine programming.
[Chess Programming Wiki](https://www.chessprogramming.org/Main_Page)
