import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random_agent
import game

player1 = random_agent.RandomAgent("Bob")
player2 = random_agent.RandomAgent("Alison")
game = game.UT3Game()
# game.print_moves = True
game.log_boards = True
game.log_prefix = "random_agents"

results = []
for i in range(10):
    results.append(game.play(player1, player2))

wins = {-1: 0., 1: 0., 0: 0.}
for r in results:
    wins[r] += 1

# print(results)
print("First player wins {} for {}%".format(wins[1], 100 * wins[1] / len(results)))
print("Second player wins {} for {} %".format(wins[-1], 100 * wins[-1] / len(results)))
print("Draws: {} for {}%".format(wins[0], 100 * wins[0] / len(results)))


exit()






def to_text(mat):
    thing = []
    for row in mat:
        r = []
        for i in row:
            if i == -1:
                r.append("O")
            elif i == 0:
                r.append(" ")
            elif i == 1:
                r.append("X")
            else:
                r.append(str(i))
        thing.append(r)
    return thing

# create board
board = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8],
                   [0, 1, 2, 3, 4, 5, 6, 7, 8],
                   [0, 1, 2, 3, 4, 5, 6, 7, 8],
                   [1, 1, 2, 3, 4, 5, 6, 7, 8],
                   [1, 1, 2, 3, 4, 5, 6, 7, 8],
                   [1, 1, 2, 3, 4, 5, 6, 7, 8],
                   [2, 1, 2, 3, 4, 5, 6, 7, 8],
                   [2, 1, 2, 3, 4, 5, 6, 7, 8],
                   [2, 1, 2, 3, 4, 5, 6, 7, 8]
                  ], int)


fig, axes = plt.subplots(nrows=3, ncols=3)

for r in range(3):
    for c in range(3):
        ax = axes[r, c]
        # hide axes
        #fig.patch.set_visible(False)
        ax.axis('off')
        # ax.axis('tight')
        d = board[r:r+3, c:c+3]
        ax.table(cellText=to_text(d), loc='center')

fig.tight_layout()

plt.show()