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
    
    def solve(self):
        pq = []
        heapq.heappush(pq, self.start)
        while len(pq) != 0:
            curr_state = heapq.heappop(pq)
            if curr_state.state in self.existing:
                continue
            else:
                self.existing.add(curr_state.state)

            if curr_state.is_goal_state(self.goal_state, self.container_list):
                return curr_state
            neighbors = curr_state.get_neighbors(self.existing, curr_state == self.start, self.goal_state, self.container_list)
            for neighbor in neighbors:
                neighbor.calc_heuristic(self.container_list, self.total_weight)
                heapq.heappush(pq, neighbor)
        return None

    def get_steps(self, final_state):
        rows = len(final_state.state)
        curr_state = final_state
        steps = []
        while curr_state != self.start:
            steps.append(curr_state.last_move)
            curr_state = curr_state.parent
        #steps.append([(rows-1, 0), (steps[len(steps)-1][0])])
        steps.reverse()
        #steps.append([(steps[len(steps)-1][1]), (rows-1, 0)])
        steps2 = [(rows-1, 0)]
        for step in steps:
            steps2.extend(step)
        steps2.append((rows-1, 0))
        steps = steps2
        for step in steps:
            print(step)
        return steps

if __name__ == "__main__":
    # SimpleTestCase4
    containers = [Container("Ship"), Container("Unused"), Container("One", 6), Container("Two", 4), Container("Three", 10)]
    start = ((1, 2, 3, 1),(1, 4, 1, 1))
    # SimpleTestCase2
    # containers = [Container("Ship"), Container("Unused"), Container("One", 10), Container("Two", 10), Container("Three", 10), Container("Four", 10)]
    # start = ((2, 3, 1, 1),(4, 5, 1, 1))
    start_state = ShipState(start, last_move = [None, (1,0)])
    rows, cols = 2, 4
    # containers, start_state = read_manifest("./Given_Test_Cases/ShipCase2.txt", rows, cols)
    solver = ShipSolver(start_state, containers)
    final_state = solver.solve()
    for i in range(rows):
        print(containers[final_state.state[i][0]].weight, containers[final_state.state[i][1]].weight, containers[final_state.state[i][2]].weight, containers[final_state.state[i][3]].weight)
    print(final_state.total_cost)
    steps = solver.get_steps(final_state)
