import nest

def create_stimuli():
    stimulus = nest.Create("poisson_generator", params={"rate": 800.0})
    return stimulus
