import unittest

import utils
from elementdata import ElementData

class TestMainWindowFunctions(unittest.TestCase):
    def setUp(self):
        # Needs to be same list of element dictionaries as used in clusterid.py
        self.elements = ElementData().elements

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
            self.assertAlmostEqual(utils.recursiveFindMass(chemical, self.elements), formulas[chemical], places=3)

    def test_flattenFormulaList(self):
        '''Tests the "flattened" formula list outputs of this utility function'''

        formulas = {'Al2O3': ['Al', 2, 'O', 3],
                    'Al2(CO)O3': ['Al', 2, 'O', 3, 'C', 1, 'O', 1],
                    'Al2O3(CO)': ['Al', 2, 'O', 3, 'C', 1, 'O', 1],
                    '(CO)Al2O3': ['Al', 2, 'O', 3, 'C', 1, 'O', 1],
                    'Al2(CO)2O3': ['Al', 2, 'O', 3, 'C', 2, 'O', 2],
                    '(H(He)(Be(Li(P))))': ['H', 1, 'He', 1, 'Be', 1, 'Li', 1, 'P', 1],
                    '((((((H(He)(Be(Li(P)))))))))': ['H', 1, 'He', 1, 'Be', 1, 'Li', 1, 'P', 1],
                    '((((((H(He)(Be(Li(P)))))))))2': ['H', 2, 'He', 2, 'Be', 2, 'Li', 2, 'P', 2],
                    '((((((H(He)(Be(Li(P))))2)))2))3': ['H', 12, 'He', 12, 'Be', 12, 'Li', 12, 'P', 12]}

        for chemical in formulas:
            self.assertListEqual(utils.flattenFormulaList(chemical), formulas[chemical], msg='Argument Used: ' + chemical)

unittest.main()
