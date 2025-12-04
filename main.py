import numpy as np
import pandas as pd
import os
import time

from ship_state import Container, ShipState
from solve import ShipSolver

def read_manifest(filename, rows=8, cols=12):
    # X2 ship has 1 bay with dim 8x12
    while True:
        while not filename.endswith(".txt"):
            filename = input("Please enter a .txt file: ")
        
        while not os.path.exists(filename):
            filename = input("Please enter a valid filename: ")

        df = pd.read_csv(filename, sep=', ', engine='python', header=None)

        if len(df) != (rows * cols):
            filename = input("Invalid manifest. Please enter a valid manifest: ")
        else:
            break

    containers = [Container("Ship"), Container("Unused")]
    num_containers = 0
    state = np.ones(shape=(rows, cols), dtype=int)

    for i in range(rows):
        for j in range(cols):
            row_idx = cols * i + j
            name_raw = df.iloc[row_idx, 2]
            if pd.isna(name_raw):
                state[i, j] = 0
                continue
            name = str(name_raw).strip()
            if name.upper() == "UNUSED":
                continue
            if name.upper() == "NAN":
                state[i, j] = 0
                continue

            weight_field = str(df.iloc[row_idx, 1]).strip()
            if weight_field.startswith('{') and weight_field.endswith('}'):
                weight_str = weight_field[1:-1]
            else:
                weight_str = weight_field
            try:
                weight = int(weight_str)
            except ValueError:
                weight = 0  # fallback

            containers.append(Container(name, weight))
            num_containers += 1
            state[i, j] = num_containers + 1

    state = tuple(map(tuple, state))
    for row in state:
        print(row)
    start_state = ShipState(state, last_move=(-1, (rows - 1, 0)))
    return containers, start_state

def make_outbound_manifest(containers, state):
    state = np.array(state)
    rows, cols = state.shape
    text = np.empty(rows * cols, dtype=str)
    lines = []
    for i in range(rows):
        for j in range(cols):
            c = containers[state[i, j]]
            text[i*cols + j] = f"[{str(i).zfill(2)}, {str(j).zfill(2)}], {{{str(c.weight).zfill(5)}}}, {c.name}"
            lines.append(f"[{str(i).zfill(2)}, {str(j).zfill(2)}], {{{str(c.weight).zfill(5)}}}, {c.name}")
    # np.savetxt(filename, text)
    return "\n".join(lines)

def main():
    filename = input("Enter the manifest file path: ")
    containers, start_state = read_manifest(filename)
    for container in containers:
        print(f"{container.name}: {container.weight}")
    start_time = time.time()
    solver = ShipSolver(start_state, containers)
    final_state = solver.solve()
    end_time = time.time()
    print(f"Solved in {end_time - start_time:.2f} seconds.")
    print(f"Final State Reached with cost {final_state.total_cost}:")
    for row in final_state.state:
        print(row)
    print("Steps taken: ")
    steps = solver.get_steps(final_state)

if __name__ == '__main__':
    main()