import unittest
from geospotter_api_py import *

class TestDummyConnector(unittest.TestCase):
    def test_GetAllNodes(self):
        api = GeoSpotterApi(useDummyConnector=True)
        res = api.GetAllNodes()
        self.assertEqual(len(res), 5)
    
    def test_SearchNodes():
        api = api = GeoSpotterApi(useDummyConnector=True)

if __name__ == "__main__":
    unittest.main()