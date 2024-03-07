import numpy as np
import matplotlib.pyplot as plt
import json
from elements.model import MultiAgent
from elements.assets import *

ROUNDS = 70
RANGE = 12
DISTANCE = 10
NUMBER_OF_AGENTS = 3
multi_agent_system = MultiAgent(number=NUMBER_OF_AGENTS, steps=ROUNDS)
IF_PLOT = True

C1_alpha = 3
C2_alpha = 2 * np.sqrt(C1_alpha)
C1_gamma = 5
C2_gamma = 0.2 * np.sqrt(C1_gamma)


game_description = "Your position is: {}. There positions of other drones are (in the format [[x, y], [x, y]...]) are: {}. "

round_description = "Your position is: {}. The positions of the other drones (in the format [[x, y], [x, y]...]) are: {}. Pick a position to move to to implement Boids flocking behavior, and briefly explain the reasoning behind your decision."

output_format = (
    "Strictly follow the &quot;Position: [x, y]&quot; format to provide your answer."
)

step = 5

for r in range(ROUNDS):
    other_agent_positions = []
    agent_position = []

    # Collect position information for the agent of interest
    agent_idx = 0  # Choose the agent index you're interested in
    agent_position = [round(multi_agent_system.agents_hist[r][agent_idx][0], 2),
                      round(multi_agent_system.agents_hist[r][agent_idx][1], 2)]
    for i in range(NUMBER_OF_AGENTS):  # Collect other agents' positions
        if i != agent_idx:
            other_agent_positions.append(
                [round(multi_agent_system.agents_hist[r][i][0], 2),
                 round(multi_agent_system.agents_hist[r][i][1], 2)])

    if (r % step) == 0:
        if r != 0:
            # Write assistant message
            with open("data2.jsonl", "a") as training_data:
                message = {
                    "messages": [
                        {"role": "assistant", "content": "Position: {}".format(agent_position)}
                    ]
                }
                training_data.write(json.dumps(message) + "\n")
            print(str(r) + " " + str(agent_idx) + " " + "assist")

    if r == 0 or (r % step) == 0:
        # Write user message
        with open("data.jsonl", "a") as training_data:
            message = {
                "messages": [
                    {"role": "user",
                     "content": ((game_description if r == 0 else round_description).format(agent_position, other_agent_positions) + " ")}
                ]
            }
            training_data.write(json.dumps(message) + "\n")
        print(str(r) + " " + str(agent_idx) + " " + "user")

    # Update multi-agent system state
    adjacency_matrix = get_adjacency_matrix(multi_agent_system.agents, RANGE)
    u = np.zeros((NUMBER_OF_AGENTS, 2))
    for i in range(NUMBER_OF_AGENTS):
        agent_p = multi_agent_system.agents[i, :2]
        agent_q = multi_agent_system.agents[i, 2:]

        neighbor_idxs = adjacency_matrix[i]
        if sum(neighbor_idxs) > 1:
            neighbors_p = multi_agent_system.agents[neighbor_idxs, :2]
            neighbors_q = multi_agent_system.agents[neighbor_idxs, 2:]
            n_ij = get_n_ij(agent_p, neighbors_p)

            term1 = C2_alpha * np.sum(phi_alpha(sigma_norm(neighbors_p - agent_p)) * n_ij, axis=0)
            a_ij = get_a_ij(agent_p, neighbors_p)
            term2 = C2_alpha * np.sum(a_ij * (neighbors_q - agent_q), axis=0)

            u_alpha = term1 + term2
        else:
            u_alpha = 0
        u_gamma = -C1_gamma * sigma_1(agent_p - [50, 50]) - C2_gamma * (agent_q - 0)
        u[i] = u_alpha + u_gamma

    multi_agent_system.update_state(u)

    if IF_PLOT:
        plt.cla()
        ax = plt.gca()
        ax.set_aspect('equal', 'box')
        plt.axis([0, 100, 0, 100])

        for i in range(NUMBER_OF_AGENTS):
            for j in range(NUMBER_OF_AGENTS):
                if i != j and adjacency_matrix[i, j] == 1:
                    plt.plot(multi_agent_system.agents[[i, j], 0], multi_agent_system.agents[[i, j], 1])

        for i, (x, y, _, _) in enumerate(multi_agent_system.agents):
            plt.scatter(x, y, c='black')

        plt.pause(0.01)

if IF_PLOT:
    plt.show()
