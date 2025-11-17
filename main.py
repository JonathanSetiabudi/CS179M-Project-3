import numpy as np
import pandas as pd
import os

from ship_state import Container, ShipState

def read_manifest(filename):
    # X2 ship has 1 bay with dim 8x12
    rows, cols = 8, 12

    while True:
        while not filename.endswith(".txt"):
            filename = input("Please enter a .txt file: ")
        
        while not os.path.exists(filename):
            filename = input("Please enter a valid filename: ")

        df = pd.read_csv(filename, sep=', ', engine='python', names=['Coordinates', 'Weight', 'Name'])

        if len(df) != (rows * cols):
            filename = input("Invalid manifest. Please enter a valid manifest: ")
        else:
            break

    # initialize list storing all containers to use indices for 2D array state
    containers = [Container("Ship"), Container("Unused")]
    num_containers = 0
    # initialize ship start state based on manifest
    state = np.ones(shape=(8, 12), dtype=int)
    for i in range(rows):
        for j in range(cols):
            name = df.iloc[(12*i) + j, 2]
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

def main():
    filename = input("Enter the manifest file path: ")
    containers, start_state = read_manifest(filename)


if __name__ == '__main__':
    main()