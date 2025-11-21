import heapq
import numpy as np
from ship_state import Container, ShipState
class ShipSolver:
    def __init__(self, start_state=None, container_list=[]):
        self.existing = set()
        self.start = start_state
        self.container_list = container_list
        self.total_weight = np.sum([container.weight for container in container_list])
        #|Ph - Sh| <= (sum(Po, So) * 0.10)
        self.goal_state = self.total_weight * 0.10

    def is_goal_state(self, ship_state):
        # Calculate the weight on the port and starboard sides
        port_weight = 0
        starboard_weight = 0
        for col in range(len(ship_state.state[0])):
            row = 0
            # While we don't find air/empty slot, keep going down the column
            # This doesn't apply to Ship slots because some containers can sit on top of the Ship slots while nothing can sit on air
            while row in range(len(ship_state.state)) and ship_state.state[row][col] != 1:
                container_index = ship_state.state[row][col]
                if container_index > 1:  # Ignore empty and unused slots
                    container = self.container_list[container_index]
                    if col < len(ship_state.state[0]) // 2:
                        port_weight += container.weight
                    else:
                        starboard_weight += container.weight
                row += 1
        # Check if the absolute difference is within the goal state threshold
        # print(f"Port Weight: {port_weight}, Starboard Weight: {starboard_weight}")
        # print(f"{abs(port_weight - starboard_weight)}")
        return abs(port_weight - starboard_weight) <= self.goal_state
    
    def solve(self):
        pq = []
        heapq.heappush(pq, self.start)
        while len(pq) != 0:
            curr_state = heapq.heappop(pq)
            for i in range(rows):
                print(containers[curr_state.state[i][0]].weight, containers[curr_state.state[i][1]].weight, containers[curr_state.state[i][2]].weight, containers[curr_state.state[i][3]].weight)
            print(f"Cost: {curr_state.total_cost}")
            if self.is_goal_state(curr_state):
                return curr_state
            neighbors = curr_state.get_neighbors(self.existing)
            for neighbor in neighbors:
                neighbor.calc_heuristic()
                heapq.heappush(pq, neighbor)
        return None

    def get_steps(self, final_state):
        rows = len(final_state.state)
        curr_state = final_state
        steps = []
        while curr_state != self.start:
            steps.append(curr_state.last_move)
            curr_state = curr_state.parent
        # print(steps)
        steps.append([(rows-1, 0), (steps[len(steps)-2][0])])
        steps.reverse()
        steps.append([(steps[len(steps)-1][1]), (rows-1, 0)])
        return steps

if __name__ == "__main__":
    containers = [Container("Ship"), Container("Unused"), Container("Ten", 10), Container("Four", 4), Container("Fourteen", 14)]
    start = ((2, 3, 1, 1),(4, 1, 1, 1))
    rows, cols = 2, 4
    start_state = ShipState(start)
    solver = ShipSolver(start_state, containers)
    final_state = solver.solve()
    for i in range(rows):
        print(containers[final_state.state[i][0]].weight, containers[final_state.state[i][1]].weight, containers[final_state.state[i][2]].weight, containers[final_state.state[i][3]].weight)
    print(final_state.total_cost)
    steps = solver.get_steps(final_state)
    print(steps)
