from ship_state import Container, ShipState
from main import read_manifest
from main import make_outbound_manifest
from ship_state import ShipState
from solve import ShipSolver
import numpy as np

def tupleConvert(obj):
    if isinstance(obj, np.ndarray):
        return obj.astype(int).tolist()
    if isinstance(obj, (list, tuple)):
        return [tupleConvert(x) for x in obj]
    if isinstance(obj, (np.int64, np.int32, np.int16, float)):
        return int(obj)
    if isinstance(obj, dict):
        return {k: tupleConvert(v) for k, v in obj.items()}
    return obj


def clean_steps(steps):
    out = []
    for pair in steps:
        out.append([int(pair[0]), int(pair[1])])
    return out

#this is necessary to make the state hashable for sets
def freeze_state(state):
    return tuple(tuple(int(x) for x in row) for row in state)

def thaw_state(state):
    return np.array(state)


def extract_ship_grids(final_state):
    grids =[]
    curr = final_state
    while curr != None:
        grids.append(curr.state)
        curr = curr.parent
    
    grids.reverse() #reverse to get from start to end
    return grids

def convert_to_jsonlist(state):
    if isinstance(state, np.ndarray): #returns whether an object is an instance or subclass of ndarray
        return state.astype(int).tolist()
    return state

def run_balancing(manifest_path):
    #load the manifest to get the containers and start state
    containers, start_state = read_manifest(manifest_path)
    
    #freeze 
    start_state.state = freeze_state(start_state.state)
    
    print("start_state.state =", start_state.state)

    #solve the problem
    solver = ShipSolver(start_state=start_state, container_list=containers)
    final_state = solver.solve()
    
    #input the final state to get the crane moves sequence (coordinates)
    if final_state is None:
        return {"solution": None}
    
    #thaw
    final_state.state = thaw_state(final_state.state)
    
    steps = solver.get_steps(final_state) #change, get_steps returns something different 
    
    newSteps = []
    rows = len(final_state.state)
    park = (rows - 1, 0) #just 7
    newSteps.append(park)
    
    for step in steps:
        newSteps.append(step["from"])
        newSteps.append(step["to"])
    newSteps.append(park)
            
    print("newSteps =", newSteps)
    print("final_state.total_cost =", final_state.total_cost)
    print("number of moves =", len(steps)) #excluding initial and final positions
    
    minutesPerMove = []
    
    for step in steps:
        minutesPerMove.append(step["crane_cost"]) 
        minutesPerMove.append(step["container_cost"])
    last = steps[-1]["to"]
    lastCost = abs(park[0] - last[0]) + abs(park[1] - last[1])
    minutesPerMove.append(lastCost)
    
    print("minutesPerMove =", minutesPerMove)
    #these are what the ship looks like at each step
    ship_grids_seq = extract_ship_grids(final_state)
    
    #convert to json
    shipstate_list_seq = [tupleConvert(s) for s in ship_grids_seq]
    
    #outbound text so the user can download file  
    outbound_text = make_outbound_manifest(containers, final_state.state)
    
    container_info = [
        {
            "index": i,
            "name": c.name,
            "weight": c.weight
        }
        for i, c in enumerate(containers)#so you can iterate through the object
    ]
    
    result = {
        "initial_state": tupleConvert(shipstate_list_seq[0]),
        "states": shipstate_list_seq,
        "steps": tupleConvert(newSteps),
        "containers": container_info,
        "moves": len(steps),  #excluding the initial and final positions
        "minutes": final_state.total_cost,
        "minutes_per_move": minutesPerMove,
        "outbound_text": outbound_text
    }
    result = tupleConvert(result)
    return result
    