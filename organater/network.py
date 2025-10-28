import nest

def create_network():
    neurons = nest.Create("hh_psc_alpha", 10)
    return neurons
