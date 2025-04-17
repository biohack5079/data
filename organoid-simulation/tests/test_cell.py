import unittest
from src.cell import Cell

class TestCell(unittest.TestCase):

    def setUp(self):
        self.cell = Cell(membrane_potential=-65)

    def test_initial_membrane_potential(self):
        self.assertEqual(self.cell.membrane_potential, -65)

    def test_update_state(self):
        self.cell.update_state(input_current=10)
        self.assertNotEqual(self.cell.membrane_potential, -65)

    def test_membrane_potential_bounds(self):
        self.cell.membrane_potential = 100
        self.cell.update_state(input_current=10)
        self.assertLessEqual(self.cell.membrane_potential, 50)

        self.cell.membrane_potential = -100
        self.cell.update_state(input_current=-10)
        self.assertGreaterEqual(self.cell.membrane_potential, -77)

if __name__ == '__main__':
    unittest.main()