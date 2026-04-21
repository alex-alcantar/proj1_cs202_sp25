import unittest
from proj1 import *

#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(0, 1, 0, 1)
        self.region = Region(self.rect, "TestRegion", "other")
        self.rc = RegionCondition(self.region, 2020, 1000, 2000.0)

    def test_emissions_per_capita_zero_pop(self):
        rc = RegionCondition(self.region, 2020, 0, 1000.0)
        self.assertEqual(emissions_per_capita(rc), 0.0)

    def test_area_wraparound(self):
        rect = GlobeRect(0, 10, 170, -170)
        self.assertTrue(area(rect) > 0)

    def test_emissions_per_square_km_zero_area(self):
        rect = GlobeRect(0, 0, 0, 0)
        region = Region(rect, "Flat", "other")
        rc = RegionCondition(region, 2020, 1000, 1000.0)
        self.assertEqual(emissions_per_square_km(rc), 0.0)

    def test_densest_multiple(self):
        rc2 = RegionCondition(self.region, 2020, 5000, 1000.0)
        self.assertEqual(densest([self.rc, rc2]), "TestRegion")

    def test_project_condition_growth(self):
        projected = project_condition(self.rc, 1)
        self.assertTrue(projected.pop >= self.rc.pop)
if __name__ == '__main__':
    unittest.main()
