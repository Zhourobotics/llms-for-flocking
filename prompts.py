class Flocking:
    agent_role = "You are a drone navigating a two-dimensional space."
    game_description = (
        "There are other drones in the space, and you must coordinate with each other to form a flock of a specified "
        "shape. Keep in mind Boids flocking rules. "
        
        "Remember to consider the positions and velocity of other drones and consider how they might behave."
        
        "Your position is: [{}]. The positions of the other drones (in the format [[x, y], [x, y]...]) are: [{}]. "
        "The maximum velocity is [{}] units per round. The flock shape is a [{}]. "
        "The minimum distance between each drone is [{}] units. "

        "You need to choose a position to move to in order to form a flock, and briefly explain "
        "the reasoning behind your decision."
    )
    round_description = (
        "You have now moved to: [{}]. The new positions of the other drones are: [{}]. "
        "Keeping in mind your maximum velocity, please select a new position to move to."
    )
    output_format = (
        "Strictly follow the 'Reasoning:..., Position: [x, y]' format to provide your answer. x and y must both be "
        "floating point numbers. Briefly provide your thought process in the reasoning section while keeping the "
        "position section ONLY for the position you wish to move to this iteration, without any further explanation."
    )

    @staticmethod
    def get_game_description(position, other_positions, max_velocity, flock_shape, safe_distance):
        return Flocking.game_description.format(
            position,
            other_positions,
            max_velocity,
            flock_shape,
            safe_distance
        )

    @staticmethod
    def get_round_description(position, other_positions):
        return Flocking.round_description.format(
            position,
            other_positions,
        )
