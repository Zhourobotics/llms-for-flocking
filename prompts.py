# Prompts from: https://github.com/WestlakeIntelligentRobotics/ConsensusLLM-code/tree/master/modules/prompt
# Personalities from: https://github.com/WestlakeIntelligentRobotics/ConsensusLLM-code/blob/master/modules/prompt/personality.py

class one_dimensional:
    agent_role = 'You are an agent moving in a one-dimensional space.'
    game_description = "There are many other agents in the space, you all need to gather at the same position, your position is: {}, other people's positions are: {}.\nYou need to choose a position to move to in order to gather, and briefly explain the reasoning behind your decision."
    round_description = "You have now moved to {}, the positions of other agents are {},\nplease choose the position you want to move to next."

class two_dimensional:
    agent_role = 'You are a robot moving in a two-dimensional space.'
    game_description = "There are many other robots in the space. You all need to gather at the same position. Your position is: {}, and the positions of others are: {}.\nChoose a position to move to in order to gather, and briefly explain the reasoning behind your decision."
    round_description = "You have now moved to {}. The positions of other robots are {}.\nPlease choose the next position you want to move to."


agent_output_form = "Strictly follow the 'Reasoning:..., Position:...' format to provide your answer.\nIn the 'Reasoning' section, it is your thought process, while the 'position' section is only the location you wish to move to in this round, without any further explanation needed."

class personality:
    stubborn = "You are an extremely stubborn person, prefer to remain stationary."
    suggestible = "You are an extremely suggestible person, prefer to move to someone else's position."