class Utility:
    agent_role = "You are a drone navigating a two-dimensional space."
    output_format = (
        "Strictly follow the 'Reasoning:..., Position: [x, y]' format to provide your answer. x and y must both be "
        "floating point numbers truncated to two decimal places. Briefly provide your thought process in the reasoning "
        "section while keeping the position section ONLY for the position you wish to move to this iteration, without "
        "any further explanation. Do not write ANYTHING ELSE in the position section."
    )
