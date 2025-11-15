import numpy as np
# Containers name + weight
class Container:
    def __init__(self, name="", weight=0):
        self.name = name
        self.weight = weight


class ShipState:
    #2D Numpy Array which represents the index of containers on the ship. 
    state = np.ones(shape=(8, 12), dtype=int)
    
    total_cost = 0
    
    parent = None
    
    last_move = []

    def __init__(self, state_array = None, total_cost = 0, parent = None, last_move = None):
        self.state = state_array
        self.total_cost = total_cost
        self.parent = parent
        self.last_move = last_move
    
    # incomplete
    def get_neighbors(self, visited_set):
        # Generate all possible next states from the current state
        neighbors = []
        top_containers = []
        for column in range(self.state.shape[1]):
            top_container = self.get_top_container(column)
            top_containers.append(top_container)
        for column in range(self.state.shape[1]):
            if top_containers[column] != -1:
                for target_column in range(self.state.shape[1]):
                    if column != target_column and not self.is_col_full(target_column):
                        tallest_row_in_btw = max(top_containers[min(column, target_column)+ 1:max(column, target_column)])
                        horizontal_distance = abs(column - target_column)
                        # 
                        height = top_containers[column]
                        target_height = top_containers[target_column] + 1
                        # standard manhattan
                        if tallest_row_in_btw < height or tallest_row_in_btw < target_height:
                            vertical_distance = abs(height - (target_height + 1))
                        # raise to go over containers
                        # tallest_row_in_btw >= target_height and tallest_row_in_btw >= height
                        else:
                            vertical_distance = abs((tallest_row_in_btw + 1) - height) + abs((tallest_row_in_btw + 1) - target_height)
                        # TODO create new state representation in new_state_array
                        new_state_array = np.copy(self.state)
        return neighbors
    
    def get_top_container(self, column):
        # Return the top container in the specified column
        for row in range(self.state.shape[0]):
            if self.state[row, column] != 0 and self.state[row, column] != -1:
                return row
        return -1
    
    def is_col_full(self, column):
        # Check if the specified column is full
        return self.state[self.state.shape[0]-1, column] != 0