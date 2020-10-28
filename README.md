# ultimate-tic-tac-toe
A framework for competitive ultimate tic-tac-toe where agents are used to compete for 

# Terms
* t3:           tic-tac-toe
* ut3:          ultimate tic-tac-toe
* board:        3x3 grid. Can be meta or local.
* local_board:  3x3 t3 grid
* meta_board:   3x3 ut3 grid that describes the 9 local board win states
* global_board: 9x9 ut3 grid

# The Game class
Keeps track of game state. Call `play()` with two agents to start a game. Before you call
play you have a few options to configure the game
* `print_moves` When true, prints the game to the console as it happens. Off by default
* `log_games` When true, logs the game move's to a log
* `log_boards` When true, will also log the game board states to the log
* `pretty_logs` Makes the logs human readable, off by default
* `log_prefix` When this is set, this will be the log prefix. The default is the name of the
given agents.

The game class is also in charge of validating the moves provided by the agent. If an 
invalid move is given, the game will end. When a local board is not declared a tie until
that local board has been filled up. In the meta-board, a tie is declared as soon as possible.

# Agents
An agent is responsible for taking a board state and making a move decision with that
information. You will implement the make_move function. When the previous move dictates
 that the agent must make a move in a certain local board, the local_board_index parameter
is how you know where to go. Give your agents logical names as you progress in your experiments.
It may be helpful to know which version of an agent was playing.

Two agents are given. The `random_agent` plays a series of random, but valid moves.
This is a useful starting point for your own agents. The `replay_agent`s will let you replay
a game from a log. This is helpful for debugging what went wrong in a game, or for playing
back a game to the console or (eventually) playing back on a game screen. The replay agents
come with a helper function that creates two agents from a log file. Make sure you give them
to the play function in the same order you got them.

# Board utilities
There are a lot of functions for analysing the game board. If there are basic helper functions
you think should be added here, feel free to. Add tests. You are not required to put any of your
own board analysis here, your secret sauce is yours.

Some of the helper functions:
* Extract a local board from the global board
* Extract the meta board from the global board
* Find out who, if anyone, has won a global board
* Find out who, if anyone, has won a local board
* Is a board still winnable by any player?
* Is a local board filled up?
* Helper functions for printing the global board and 3x3 boards
* Getting boards and moves from a log file

When looking at the global board, 1 is the player who went first (X) and -1 is the player
who went second (O). 0 in a global or local board means no move has been made. In the metaboard,
0 means a tie, and None means that local game isn't determined yet.

# Logs
The logs tell you what happened in a game, and if you're using machine learning, will serve
as your training data. The logs record what time the `play()` function was called, the names of the 
agents, who won, and the list of moves taken. The agent listed first is the agent that made the first move.

By default, the moves are stored without board state since that can recreated from the moves. The helper function 
`get_data_from_log` in `board_utils` recreates the board states if they aren't saved. Since we will likely want 
thousands of these, I didn't want file IO to botteneck generating training data.
It's possible that it would be faster to just store the board states, feel free to run an experiment to prove this was a 
bad idea. Use the `log_boards` flag to turn board saving on.

By default, the logs will be named with the names of the two agents, appended with a timestamp. This keeps
log names reasonably unique, unless you are running multiple games at the same time. If you do this, be sure
to change the agent names, or set the `log_prefix` to something that distinguishes the games. It also orders the logs
in chronological order in your file explorer.

You don't have to upload your logs, or even save them to the default directory. I put them under `./logs/`
just for convenience.