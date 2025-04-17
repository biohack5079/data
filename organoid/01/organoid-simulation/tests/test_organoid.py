import unittest
from src.organoid import Organoid

class TestOrganoid(unittest.TestCase):

    def setUp(self):
        self.organoid = Organoid(num_cells=50)  # Initialize an organoid with 50 cells

    def test_initialization(self):
        self.assertEqual(len(self.organoid.cells), 50)
        for cell in self.organoid.cells:
            self.assertIsNotNone(cell.membrane_potential)

    def test_run_simulation(self):
        initial_state = self.organoid.get_state()
        self.organoid.run_simulation(time=100)
        final_state = self.organoid.get_state()
        self.assertNotEqual(initial_state, final_state)

    def test_cell_interaction(self):
        self.organoid.run_simulation(time=100)
        # Check if cells have interacted (this will depend on your implementation)
        for i in range(len(self.organoid.cells) - 1):
            self.assertNotEqual(self.organoid.cells[i].membrane_potential, 
                                self.organoid.cells[i + 1].membrane_potential)

if __name__ == '__main__':
    unittest.main()