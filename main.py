import numpy as np
import matplotlib.pyplot as plt
from elements.model import MultiAgent
from elements.assets import *

ROUNDS = 60
RANGE = 12
DISTANCE = 10
NUMBER_OF_AGENTS = 4
multi_agent_system = MultiAgent(number=NUMBER_OF_AGENTS, steps=ROUNDS)
IF_PLOT = True

C1_alpha = 3
C2_alpha = 2 * np.sqrt(C1_alpha)
C1_gamma = 5
C2_gamma = 0.2 * np.sqrt(C1_gamma)


game_description = "Your position is: {}. There are other drones in this space and their positions (in the format [[x, y], [x, y]...]) are: {}. Your collective task are to implement a flocking behavior. Keep in mind Boids flocking rules. Consider the velocity of the agents by calculating their distance traveled over the last few rounds. Attempt to match the velocity of nearby agents and adjust your movement to align with this average direction. Consider what are the distances between you and the other drones? If they are too close, you must move away to maintain personal space, otherwise you will fail the task. Finally, if you are not near any other agents, move towards the center of mass of nearby agents to stay close to the group."

round_description = "Your position is: {}. The positions of the other drones (in the format [[x, y], [x, y]...]) are: {}. Pick a position to move to to implement Boids flocking behavior, and briefly explain the reasoning behind your decision."

output_format = (
    "Strictly follow the &quot;Position: [x, y]&quot; format to provide your answer. x and y must both be "
    "floating point numbers truncated to two decimal places. Do not write ANYTHING ELSE in the position section."
)

# plotting agents
for t in range(ROUNDS):
    adjacency_matrix = get_adjacency_matrix(multi_agent_system.agents, RANGE)
    u = np.zeros((NUMBER_OF_AGENTS,2))
    for i in range(NUMBER_OF_AGENTS):
        agent_p = multi_agent_system.agents[i,:2]
        agent_q = multi_agent_system.agents[i,2:]
        # term1
        neighbor_idxs = adjacency_matrix[i]
        if sum(neighbor_idxs)>1:
            neighbors_p = multi_agent_system.agents[neighbor_idxs,:2]
            neighbors_q = multi_agent_system.agents[neighbor_idxs,2:]
            n_ij = get_n_ij(agent_p, neighbors_p)

            term1 = C2_alpha * np.sum(phi_alpha(sigma_norm(neighbors_p-agent_p))*n_ij, axis=0)
            # term2
            a_ij = get_a_ij(agent_p, neighbors_p)
            term2 = C2_alpha * np.sum(a_ij*(neighbors_q-agent_q), axis=0)

            # u_alpha
            u_alpha = term1 + term2
        else:
            u_alpha=0
        u_gamma = -C1_gamma*sigma_1(agent_p-[50,50]) -C2_gamma*(agent_q-0)
        u[i] = u_alpha+u_gamma


    
    multi_agent_system.update_state(u)
    
    if IF_PLOT:
        plt.cla()
        ax = plt.gca()
        ax.set_aspect('equal', 'box')
        plt.axis([0, 100, 0, 100])
        

        for i in range(NUMBER_OF_AGENTS):
            for j in range(NUMBER_OF_AGENTS):
                if i!= j and adjacency_matrix[i,j] == 1:
                    plt.plot(multi_agent_system.agents[[i,j],0], multi_agent_system.agents[[i,j],1])

        for i, (x, y,_,_) in enumerate(multi_agent_system.agents):
            plt.scatter(x, y, c='black')

        plt.pause(0.01)



data = [[{"role": "system", "content": "You are a drone navigating a two-dimensional space."}]] * NUMBER_OF_AGENTS

step = 4

for r in range(ROUNDS):
    for a in range(NUMBER_OF_AGENTS):
        other_agent_positions = []
        agent_position = []
        
        for i in range(NUMBER_OF_AGENTS): # other agents
            if i == a:
                agent_position = [round(multi_agent_system.agents_hist[r][i][0], 2), round(multi_agent_system.agents_hist[r][i][1], 2)]
            else:
                other_agent_positions.append([round(multi_agent_system.agents_hist[r][i][0], 2), round(multi_agent_system.agents_hist[r][i][1], 2)])
        
        if (r) % step == 0:
            if (r != 0):
                data[a].extend([{"role": "assistant", "content": "Position: {}".format(agent_position)}])
                print(str(r) + " " + str(a) + " " + "assist")
        
        if r == 0 or ((r) % step == 0):
            data[a].extend([{"role": "user", "content": ((game_description if r == 0 else round_description).format(agent_position,other_agent_positions) + " " + output_format)}])
            print(str(r) + " " + str(a) + " " + "user")


with open("data.jsonl", "a") as training_data:
    for a in range(len(data)):                
        message = str('{"messages": ' + str(data[a][:-1]) + '}').replace("'", '"').replace('\\"', '"').replace("&quot;", "'")  # lol python
        training_data.write(message + "\n")

if IF_PLOT:
    plt.show()
