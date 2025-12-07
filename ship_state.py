import numpy as np
# Containers name + weight
class Container:
    def __init__(self, name="", weight=0):
        self.name = name
        self.weight = weight

class ShipState:
    #2D Numpy Array which represents the index of containers on the ship. 
    def __init__(self, state_array = None, total_cost = 0, parent = None, last_move = None):
        self.state = state_array
        self.total_cost = total_cost
        self.parent = parent
        self.last_move = last_move
        self.heuristic = 0

    def __lt__(self, other):
        return self.total_cost + self.heuristic < other.total_cost + other.heuristic
    
    def is_goal_state(self, goal_state, container_list):
        # Trivially balanced if there are only 2 or 3 containers (Ship and Unused and (maybe) + 1 container)
        if len(container_list) == 2 or len(container_list) == 3:
            return True
        # if there are two containers besides Ship and Unused, make sure they're on opposite sides
        elif len(container_list) == 4:
            port_has_container = False
            starboard_has_container = False
            for col in range(len(self.state[0])):
                if self.state[self.get_top_container(col)][col] > 1:
                    if col < len(self.state[0]) // 2:
                        port_has_container = True
                    else:
                        starboard_has_container = True

            return port_has_container and starboard_has_container
        # Calculate the weight on the port and starboard sides
        port_weight = 0
        starboard_weight = 0
        for col in range(len(self.state[0])):
            row = 0
            # While we don't find air/empty slot, keep going up the column
            # This doesn't apply to Ship slots because some containers can sit on top of the Ship slots while nothing can sit on air
            while row in range(len(self.state)) and self.state[row][col] != 1:
                container_index = self.state[row][col]
                if container_index > 1:  # Ignore empty and unused slots
                    container = container_list[container_index]
                    if col < len(self.state[0]) // 2:
                        port_weight += container.weight
                    else:
                        starboard_weight += container.weight
                row += 1

        return abs(port_weight - starboard_weight) <= goal_state

    # Returns an 3D Numpy Array of all possible next states from the current state
    def get_neighbors(self, visited_set, is_start, goal_state, container_list):
        def get_tallest_in_between(col1, col2, top_containers):
            if abs(col2 - col1) <= 1:
                return -1
            return max(top_containers[min(col1, col2)+1:max(col1, col2)])
        
        def get_vertical_distance(height, target_height, tallest_in_btw):
            # standard manhattan
            if tallest_in_btw < height or tallest_in_btw < target_height:
                return abs(height - (target_height))
            # raise to go over containers
            # tallest_row_in_btw >= target_height and tallest_row_in_btw >= height
            else:
                return abs((tallest_in_btw + 1) - height) + abs((tallest_in_btw + 1) - target_height)
        curr_state = np.array(self.state)
        neighbors = []
        top_containers = []

        # get possible containers to move
        for column in range(curr_state.shape[1]):
            top_container = self.get_top_container(column)
            top_containers.append(top_container)

        for column in range(curr_state.shape[1]):
            if top_containers[column] != -1 and (is_start or self.last_move[1] != (top_containers[column], column)):
                # move container if possible
                for target_column in range(curr_state.shape[1]):
                    if column != target_column and not self.is_col_full(target_column):
                        # Calculate vertical and horizontal distance between two positions
                        tallest_row_in_btw = get_tallest_in_between(column, target_column, top_containers)
                        horizontal_distance = abs(column - target_column)
                        height = top_containers[column]
                        target_height = top_containers[target_column] + 1
                        vertical_distance = get_vertical_distance(height, target_height, tallest_row_in_btw)
                        new_state_array = np.copy(curr_state)
                        # Move container from column to target_column
                        new_state_array[target_height, target_column], new_state_array[height, column] = new_state_array[height, column], new_state_array[target_height, target_column]
                        new_state_array = tuple(map (tuple, new_state_array))
                        if new_state_array in visited_set:
                            continue
                        move_cost = horizontal_distance + vertical_distance
                        move_from_prev = 0
                        if is_start:
                            # Add extra cost for moving from parking position
                            move_cost += column + len(self.state) - 1 - height
                        else:
                            # Add cost moving from last move to this column
                            prev_row = self.last_move[1][0]
                            prev_col = self.last_move[1][1]
                            tallest_between_prev = get_tallest_in_between(prev_col, column, top_containers)
                            horizontal_from_prev = abs(prev_col - column)
                            vertical_from_prev = get_vertical_distance(prev_row, height, tallest_between_prev)
                            move_from_prev = horizontal_from_prev + vertical_from_prev
                            move_cost += move_from_prev
                            
                        new_state = ShipState(new_state_array, self.total_cost + move_cost, self, [(height, column), (target_height, target_column)])
                        if new_state.is_goal_state(goal_state, container_list):
                            new_state.total_cost += (len(self.state)-1) - new_state.last_move[1][0] + new_state.last_move[1][1]
                        neighbors.append(new_state)       
        return neighbors
    
    def get_top_container(self, column):
        # Return the top container in the specified column
        row = len(self.state)-1
        while row in range(len(self.state)) and self.state[row][column] == 1:
            row -= 1
        return row
    
    def is_col_full(self, column):
        # Check if the specified column is full
        return self.state[len(self.state)-1][column] != 1 and self.state[len(self.state)-1][column] != 0
    
    def calc_heuristic(self, container_list, total_weight):
        port_weight = 0
        starboard_weight = 0
        port_list = []
        starboard_list = []
        for col in range(len(self.state[0])):
            row = 0
            # While we don't find air/empty slot, keep going down the column
            # This doesn't apply to Ship slots because some containers can sit on top of the Ship slots while nothing can sit on air
            while row in range(len(self.state)) and self.state[row][col] != 1:
                container_index = self.state[row][col]
                if container_index > 1:  # Ignore empty and unused slots
                    container = container_list[container_index]
                    if col < len(self.state[0]) // 2:
                        port_weight += container.weight
                        port_list.append((container, col))
                    else:
                        starboard_weight += container.weight
                        starboard_list.append((container, col))
                row += 1
        balance_mass = total_weight / 2
        deficit = balance_mass - min(port_weight, starboard_weight)
        port_heavier = port_weight > starboard_weight
        if port_heavier:
            port_list = sorted(port_list, key = lambda x: x[0].weight, reverse=True)
            i = 0
            while i < len(port_list) and port_list[i][0].weight > deficit:
                i += 1
            if i < len(port_list):
                nearest_starboard = len(self.state[0]) // 2
                while nearest_starboard < len(self.state[0]) and self.is_col_full(nearest_starboard):
                    nearest_starboard += 1
                self.heuristic = abs(nearest_starboard - port_list[i][1])
            else:
                self.heuristic = 0
        else:
            starboard_list = sorted(starboard_list, key = lambda x: x[0].weight, reverse=True)
            i = 0
            while i < len(starboard_list) and starboard_list[i][0].weight > deficit:
                i += 1
            if i < len(starboard_list):
                nearest_port = len(self.state[0]) // 2 - 1
                while nearest_port >= 0 and self.is_col_full(nearest_port):
                    nearest_port -= 1
                self.heuristic = abs(starboard_list[i][1] - nearest_port)
            else:
                self.heuristic = 0
        return
    
if __name__ == "__main__":
    containers = [Container("Ship"), Container("Unused"), Container("Ten", 10), Container("Four", 4), Container("Fourteen", 14)]
    start = ((2, 3, 1, 1),(4, 1, 1, 1))
    rows, cols = 2, 4
    visited = set()
    visited.add(start)
    start_state = ShipState(start)
    neighbors = start_state.get_neighbors(visited)
    for neighbor in neighbors:
        for i in range(rows):
            print(containers[neighbor.state[i][0]].weight, containers[neighbor.state[i][1]].weight, containers[neighbor.state[i][2]].weight, containers[neighbor.state[i][3]].weight)
        print()