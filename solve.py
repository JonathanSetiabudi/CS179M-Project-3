import numpy as np

class Solve:
    # stores already visited states
    existing = set()
    
    # stores the starting state by default will contain the goal state and will be set to the
    # actual starting state in the constructor
    start = None
    
    total_weight = 0

    container_list = []

    # Balance state of the ship 
    goal_state = 0

    def __init__(self, start_state, container_list):
        self.start = start_state
        self.container_list = container_list
        self.total_weight = np.sum([container.weight for container in container_list])
        #|Ph - Sh| <= (sum(Po, So) * 0.10)
        self.goal_state = self.total_weight * 0.10

    def is_goal_state(self, ship_state):
        # Calculate the weight on the port and starboard sides
        port_weight = 0
        starboard_weight = 0
        for col in range(ship_state.state.shape[1]):
            row = 0
            # While we don't find air/empty slot, keep going down the column
            # This doesn't apply to Ship slots because some containers can sit on top of the Ship slots while nothing can sit on air
            while row in range(ship_state.state.shape[0]) and ship_state.state[row, col] != 1:
                container_index = ship_state.state[row, col]
                if container_index > 1:  # Ignore empty and unused slots
                    container = self.container_list[container_index]
                    if col < ship_state.state.shape[1] // 2:
                        port_weight += container.weight
                    else:
                        starboard_weight += container.weight
        # Check if the absolute difference is within the goal state threshold
        return abs(port_weight - starboard_weight) <= self.goal_state