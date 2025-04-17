from cell import Cell  # Cellクラスをインポート

class Organoid:
    def __init__(self, num_cells):
        self.cells = [Cell() for _ in range(num_cells)]

    def initialize(self):
        for cell in self.cells:
            cell.initialize()

    def run_simulation(self, time_steps):
        for t in range(time_steps):
            for cell in self.cells:
                cell.update_state(self.cells)

    def get_membrane_potentials(self):
        return [cell.membrane_potential for cell in self.cells]
    
    def update_cells(self, time_interval):
        for cell in self.cells:
            cell.update(time_interval)

    def collect_data(self):
        return [cell.get_state() for cell in self.cells]