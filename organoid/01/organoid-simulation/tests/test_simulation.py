import unittest
from src.simulation import Simulation

class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.simulation = Simulation(num_cells=50)  # Initialize with 50 cells

    def test_initialization(self):
        self.assertEqual(len(self.simulation.organoid.cells), 50)
        self.assertIsNotNone(self.simulation.organoid)

    def test_run_simulation(self):
        results = self.simulation.run(time_steps=100)
        self.assertEqual(len(results), 100)
        self.assertTrue(all(isinstance(result, list) for result in results))

    def test_data_collection(self):
        self.simulation.run(time_steps=100)
        data = self.simulation.collect_data()
        self.assertIn('membrane_potentials', data)
        self.assertEqual(len(data['membrane_potentials']), 100)

if __name__ == '__main__':
    unittest.main()