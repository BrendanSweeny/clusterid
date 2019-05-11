import unittest

from clusterid import MainWindow as MW

class TestMainWindowFunctions(unittest.TestCase):
    def setUp(self):
        self.test_MW = MW()

    def test_recursiveFindMass(self):
        '''Test the accuracy of the recursiveFindMass function
        on chemical formulas formatted with parentheses in various ways'''

        formulas = {'Al2O3': 101.961,
                    'Al2(CO)O3': 129.971,
                    'Al2O3(CO)': 129.971,
                    '(CO)Al2O3': 129.971,
                    'Al2(CO)2O3': 157.981,
                    '(H(He)(Be(Li(P))))': 51.938,
                    '((((((H(He)(Be(Li(P)))))))))': 51.938,
                    '((((((H(He)(Be(Li(P)))))))))2': 103.876,
                    '((((((H(He)(Be(Li(P))))2)))2))3': 623.256}

        for chemical in formulas:
            self.assertAlmostEqual(self.test_MW.recursiveFindMass(chemical), formulas[chemical], places=3)

unittest.main()
