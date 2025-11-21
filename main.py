import numpy as np
import pandas as pd
import os

from ship_state import Container, ShipState
# from solve import ShipSolver

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

    # initialize list storing all containers to use indices for 2D array state
    containers = [Container("Ship"), Container("Unused")]
    num_containers = 0
    # initialize ship start state based on manifest
    state = np.ones(shape=(rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            name = df.iloc[(cols*i) + j, 2]
            if name == "UNUSED":
                continue
            if name == "NAN":
                state[i, j] = 0
            else:
                weight = int(df.iloc[i, 1][1:6])
                containers.append(Container(name, weight))
                num_containers += 1
                state[i, j] = num_containers + 1
    print(state)
    start_state = ShipState(state)
    return containers, start_state

def make_outbound_manifest(filename, containers, state):
    state = np.array(state)
    rows, cols = state.shape[0], state.shape[1]
    text = np.empty(rows * cols, dtype=str)
    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            text[i*cols + j] = f"[{str(i).zfill(2)}, {str(j).zfill(2)}], {{{str(containers[state[i, j]].weight).zfill(5)}}}, {containers[state[i, j]].name}"
    np.savetxt(filename, text)

def main():
    filename = input("Enter the manifest file path: ")
    containers, start_state = read_manifest(filename)
    

if __name__ == '__main__':
    main()