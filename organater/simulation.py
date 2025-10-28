import nest
from network import create_network
from stimuli import create_stimuli
from recorder import setup_recorders
from utils import log

def run_simulation():
    nest.ResetKernel()
    log("Organater simulation started.")

    neurons = create_network()
    stimuli = create_stimuli()
    recorders = setup_recorders()

    # 接続処理（仮）
    # nest.Connect(stimuli, neurons)
    # nest.Connect(neurons, recorders)

    nest.Simulate(100.0)
    log("Simulation completed.")

if __name__ == '__main__':
    run_simulation()
