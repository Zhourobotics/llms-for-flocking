class Flocking:
    # agent_role = "You are a drone navigating a two-dimensional space."
    # game_description = (
    #     "There are other drones in the space, and you must coordinate with each other to form a flock of a specified "
    #     "shape. Keep in mind Boids flocking rules. "
        
    #     "Your position is: [{}]. The positions of the other drones (in the format [[x, y], [x, y]...]) are: [{}]. "
    #     "The maximum velocity is [{}] units per round. The flock shape is a [{}]. "
        
    #     "You must avoid getting closer than [{}] units to any peers, otherwise you may collide. "
        
    #     "Remember to consider the positions and velocity of other drones and consider how they might behave. "

    #     "You need to choose a position to move to in order to form a flock, and briefly explain "
    #     "the reasoning behind your decision."
    # )
    # round_description = (
    #     "You have now moved to: [{}]. The new positions of the other drones are: [{}]. "
    #     "Consider how well your strategy worked last round, keeping in mind your maximum velocity, "
    #     "please select a new position to move to."
    # )
    # output_format = (
    #     "Strictly follow the 'Reasoning:..., Position: [x, y]' format to provide your answer. x and y must both be "
    #     "floating point numbers truncated to two decimal places. Briefly provide your thought process in the reasoning "
    #     "section while keeping the position section ONLY for the position you wish to move to this iteration, without "
    #     "any further explanation. Do not write ANYTHING ELSE in the position section."
    # )
    agent_role = "You are a drone in a two-dimensional space. You will form a flock by keeping a desired distance between your nearest few neighbors. Your position will be provided as [x, y]. There are other drones in this space with positions in the format [[x1, y1], [x2, y2], ...]. We will only provide the information for the neighbors within the communication range, which is 12 units away. You should keep an ideal distance of 10 units away from your neighbor."
    game_description = (
        "There are other drones in the space, and you must coordinate with each other to form a flock of a specified "
        "shape. Keep in mind Boids flocking rules. "
        
        "Your position is: [{}]. The positions of the other drones (in the format [[x, y], [x, y]...]) are: [{}]. "
        "The maximum velocity is [{}] units per round. The flock shape is a [{}]. "
        
        "You must avoid getting closer than [{}] units to any peers, otherwise you may collide. "
        
        "Remember to consider the positions and velocity of other drones and consider how they might behave. "

        "You need to choose a position to move to in order to form a flock, and briefly explain "
        "the reasoning behind your decision."
    )
    round_description = (
        "Your position is: {}. Your neighbors positions are: {}."
    )
    # output_format = (
    #     "Strictly follow the 'Reasoning:..., Position: [x, y]' format to provide your answer. x and y must both be "
    #     "floating point numbers truncated to two decimal places. Briefly provide your thought process in the reasoning "
    #     "section while keeping the position section ONLY for the position you wish to move to this iteration, without "
    #     "any further explanation. Do not write ANYTHING ELSE in the position section."
    # )
    output_format = (
        "Only provide your response in 'Position: [x, y]' format. x and y must both be floating point numbers truncated to two decimal places."
    )