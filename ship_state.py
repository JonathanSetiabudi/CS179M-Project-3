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

    # Returns an 3D Numpy Array of all possible next states from the current state
    def get_neighbors(self, visited_set):
        curr_state = np.array(self.state)
        neighbors = []
        top_containers = []

        # get possible containers to move
        for column in range(curr_state.shape[1]):
            top_container = self.get_top_container(column)
            top_containers.append(top_container)

        for column in range(curr_state.shape[1]):
            if top_containers[column] != -1:
                # move container if possible
                for target_column in range(curr_state.shape[1]):
                    if column != target_column and not self.is_col_full(target_column):
                        tallest_row_in_btw = 0
                        if abs(target_column - column) > 1:
                            tallest_row_in_btw = max(top_containers[min(column, target_column)+1:max(column, target_column)])
                        horizontal_distance = abs(column - target_column)
                        
                        height = top_containers[column]
                        target_height = top_containers[target_column] + 1
                        # standard manhattan
                        if tallest_row_in_btw < height or tallest_row_in_btw < target_height:
                            vertical_distance = abs(height - (target_height))
                        # raise to go over containers
                        # tallest_row_in_btw >= target_height and tallest_row_in_btw >= height
                        else:
                            vertical_distance = abs((tallest_row_in_btw + 1) - height) + abs((tallest_row_in_btw + 1) - target_height)
                        new_state_array = np.copy(curr_state)
                        # Move container from column to target_column
                        new_state_array[target_height, target_column] = new_state_array[height, column]
                        new_state_array[height, column] = 1
                        new_state_array = tuple(map (tuple, new_state_array))
                        if new_state_array in visited_set:
                            continue
                        move_cost = horizontal_distance + vertical_distance
                        new_state = ShipState(new_state_array, self.total_cost + move_cost, self, [(height, column), (target_height, target_column)])
                        neighbors.append(new_state)       
        return neighbors
    
    def get_top_container(self, column):
        # Return the top container in the specified column
        for row in range(len(self.state)-1, -1, -1):
            if self.state[row][column] != 0 and self.state[row][column] != 1:
                return row
        return -1
    
    def is_col_full(self, column):
        # Check if the specified column is full
        return self.state[len(self.state)-1][column] != 1
    
    def calc_heuristic(self):
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