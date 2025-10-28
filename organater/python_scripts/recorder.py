import nest

def setup_recorders():
    voltmeter = nest.Create("voltmeter")
    spike_detector = nest.Create("spike_detector")
    return {"voltmeter": voltmeter, "spike_detector": spike_detector}
