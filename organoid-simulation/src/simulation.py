print("Simulation script started")

class Simulation:
    def __init__(self, num_cells, time_steps, time_interval):
        self.num_cells = num_cells
        self.time_steps = time_steps
        self.time_interval = time_interval
        self.organoid = None
        self.data = []

    def initialize_organoid(self):
        from organoid import Organoid
        self.organoid = Organoid(self.num_cells)
        self.organoid.initialize() 
    def run(self):
        print("Simulation is running")
        self.initialize_organoid()
        for step in range(self.time_steps):
            self.organoid.update_cells(self.time_interval)
            self.data.append(self.organoid.collect_data())

    def get_results(self):
        return self.data


if __name__ == "__main__":
    sim = Simulation(num_cells=10, time_steps=100, time_interval=0.1)
    sim.run()
    results = sim.get_results()
    print("Simulation completed. Results:", results)