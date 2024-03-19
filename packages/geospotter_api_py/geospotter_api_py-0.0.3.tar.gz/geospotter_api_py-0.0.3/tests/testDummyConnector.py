import unittest
from geospotter_api_py import *

class testDummyConnector(unittest.TestCase):
    def test_GetAllNodes(self):
        api = GeoSpotterApi(useDummyConnector=True)
        res = api.GetAllNodes()
        self.assertEqual(len(res), 5)
    
    def test_SearchNodes(self):
        api =  GeoSpotterApi(useDummyConnector=True)
        res = api.SearchNodes("Camerino")
        self.assertEqual(len(res),2)
        res = api.SearchNodes("Cam")
        self.assertEqual(len(res),2)
        res = api.SearchNodes("castel")
        self.assertEqual(len(res),3,msg=res)

if __name__ == "__main__":
    unittest.main()