# TODO: Add a 'custom field' to periodic table to define a molecule or ligand
# and specify a mass for the ligand to be added to selected masses list
# TODO: Consider adding a filter to the target mass output
# TODO: look into plotting isotope patterns for a clicked species in the
# target mass output, make periodic table and plot as separate tabs

import sys
import re
import images_qr
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtGui import QIcon
from clusteridui import Ui_ClusterID

import math
from operator import attrgetter, itemgetter
from elements import Element

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.elements = [
          {
            "number": 1,
            "mass": 1.008,
            "name": "Hydrogen",
            "symbol": "H",
            "mp": -259.0,
            "bp": -253.0,
            "density": 0.09,
            "group": 1.0,
            "config": "1s1",
            "IE": 13.6,
			"isotopes": ((1.008, 0.999885), (2.014, 0.000115))
          },
          {
            "number": 2,
            "mass": 4.003,
            "name": "Helium",
            "symbol": "He",
            "mp": -272.0,
            "bp": -269.0,
            "density": 0.18,
            "group": 18.0,
            "config": "1s2",
            "IE": 24.59,
			"isotopes": ((3.016, 0.000001), (4.003, 0.999999))
          },
          {
            "number": 3,
            "mass": 6.941,
            "name": "Lithium",
            "symbol": "Li",
            "mp": 180.0,
            "bp": 1347.0,
            "density": 0.53,
            "group": 1.0,
            "config": "[He] 2s1",
            "IE": 5.39,
			"isotopes": ((6.015, 0.0759), (7.016, 0.9241))
          },
          {
            "number": 4,
            "mass": 9.012,
            "name": "Beryllium",
            "symbol": "Be",
            "mp": 1278.0,
            "bp": 2970.0,
            "density": 1.85,
            "group": 2.0,
            "config": "[He] 2s2",
            "IE": 9.32
          },
          {
            "number": 5,
            "mass": 10.811,
            "name": "Boron",
            "symbol": "B",
            "mp": 2300.0,
            "bp": 2550.0,
            "density": 2.34,
            "group": 13.0,
            "config": "[He] 2s2 2p1",
            "IE": 8.3
          },
          {
            "number": 6,
            "mass": 12.011,
            "name": "Carbon",
            "symbol": "C",
            "mp": 3500.0,
            "bp": 4827.0,
            "density": 2.26,
            "group": 14.0,
            "config": "[He] 2s2 2p2",
            "IE": 11.26
          },
          {
            "number": 7,
            "mass": 14.007,
            "name": "Nitrogen",
            "symbol": "N",
            "mp": -210.0,
            "bp": -196.0,
            "density": 1.25,
            "group": 15.0,
            "config": "[He] 2s2 2p3",
            "IE": 14.53
          },
          {
            "number": 8,
            "mass": 15.999,
            "name": "Oxygen",
            "symbol": "O",
            "mp": -218.0,
            "bp": -183.0,
            "density": 1.43,
            "group": 16.0,
            "config": "[He] 2s2 2p4",
            "IE": 13.62
          },
          {
            "number": 9,
            "mass": 18.998,
            "name": "Fluorine",
            "symbol": "F",
            "mp": -220.0,
            "bp": -188.0,
            "density": 1.7,
            "group": 17.0,
            "config": "[He] 2s2 2p5",
            "IE": 17.42
          },
          {
            "number": 10,
            "mass": 20.18,
            "name": "Neon",
            "symbol": "Ne",
            "mp": -249.0,
            "bp": -246.0,
            "density": 0.9,
            "group": 18.0,
            "config": "[He] 2s2 2p6",
            "IE": 21.56
          },
          {
            "number": 11,
            "mass": 22.99,
            "name": "Sodium",
            "symbol": "Na",
            "mp": 98.0,
            "bp": 883.0,
            "density": 0.97,
            "group": 1.0,
            "config": "[Ne] 3s1",
            "IE": 5.14
          },
          {
            "number": 12,
            "mass": 24.305,
            "name": "Magnesium",
            "symbol": "Mg",
            "mp": 639.0,
            "bp": 1090.0,
            "density": 1.74,
            "group": 2.0,
            "config": "[Ne] 3s2",
            "IE": 7.65
          },
          {
            "number": 13,
            "mass": 26.982,
            "name": "Aluminum",
            "symbol": "Al",
            "mp": 660.0,
            "bp": 2467.0,
            "density": 2.7,
            "group": 13.0,
            "config": "[Ne] 3s2 3p1",
            "IE": 5.99
          },
          {
            "number": 14,
            "mass": 28.086,
            "name": "Silicon",
            "symbol": "Si",
            "mp": 1410.0,
            "bp": 2355.0,
            "density": 2.33,
            "group": 14.0,
            "config": "[Ne] 3s2 3p2",
            "IE": 8.15
          },
          {
            "number": 15,
            "mass": 30.974,
            "name": "Phosphorus",
            "symbol": "P",
            "mp": 44.0,
            "bp": 280.0,
            "density": 1.82,
            "group": 15.0,
            "config": "[Ne] 3s2 3p3",
            "IE": 10.49
          },
          {
            "number": 16,
            "mass": 32.065,
            "name": "Sulfur",
            "symbol": "S",
            "mp": 113.0,
            "bp": 445.0,
            "density": 2.07,
            "group": 16.0,
            "config": "[Ne] 3s2 3p4",
            "IE": 10.36
          },
          {
            "number": 17,
            "mass": 35.453,
            "name": "Chlorine",
            "symbol": "Cl",
            "mp": -101.0,
            "bp": -35.0,
            "density": 3.21,
            "group": 17.0,
            "config": "[Ne] 3s2 3p5",
            "IE": 12.97
          },
          {
            "number": 18,
            "mass": 39.948,
            "name": "Argon",
            "symbol": "Ar",
            "mp": -189.0,
            "bp": -186.0,
            "density": 1.78,
            "group": 18.0,
            "config": "[Ne] 3s2 3p6",
            "IE": 15.76
          },
          {
            "number": 19,
            "mass": 39.098,
            "name": "Potassium",
            "symbol": "K",
            "mp": 64.0,
            "bp": 774.0,
            "density": 0.86,
            "group": 1.0,
            "config": "[Ar] 4s1",
            "IE": 4.34
          },
          {
            "number": 20,
            "mass": 40.078,
            "name": "Calcium",
            "symbol": "Ca",
            "mp": 839.0,
            "bp": 1484.0,
            "density": 1.55,
            "group": 2.0,
            "config": "[Ar] 4s2",
            "IE": 6.11
          },
          {
            "number": 21,
            "mass": 44.956,
            "name": "Scandium",
            "symbol": "Sc",
            "mp": 1539.0,
            "bp": 2832.0,
            "density": 2.99,
            "group": 3.0,
            "config": "[Ar] 3d1 4s2",
            "IE": 6.56
          },
          {
            "number": 22,
            "mass": 47.867,
            "name": "Titanium",
            "symbol": "Ti",
            "mp": 1660.0,
            "bp": 3287.0,
            "density": 4.54,
            "group": 4.0,
            "config": "[Ar] 3d2 4s2",
            "IE": 6.83
          },
          {
            "number": 23,
            "mass": 50.942,
            "name": "Vanadium",
            "symbol": "V",
            "mp": 1890.0,
            "bp": 3380.0,
            "density": 6.11,
            "group": 5.0,
            "config": "[Ar] 3d3 4s2",
            "IE": 6.75
          },
          {
            "number": 24,
            "mass": 51.996,
            "name": "Chromium",
            "symbol": "Cr",
            "mp": 1857.0,
            "bp": 2672.0,
            "density": 7.19,
            "group": 6.0,
            "config": "[Ar] 3d5 4s1",
            "IE": 6.77
          },
          {
            "number": 25,
            "mass": 54.938,
            "name": "Manganese",
            "symbol": "Mn",
            "mp": 1245.0,
            "bp": 1962.0,
            "density": 7.43,
            "group": 7.0,
            "config": "[Ar] 3d5 4s2",
            "IE": 7.43
          },
          {
            "number": 26,
            "mass": 55.845,
            "name": "Iron",
            "symbol": "Fe",
            "mp": 1535.0,
            "bp": 2750.0,
            "density": 7.87,
            "group": 8.0,
            "config": "[Ar] 3d6 4s2",
            "IE": 7.9
          },
          {
            "number": 27,
            "mass": 58.933,
            "name": "Cobalt",
            "symbol": "Co",
            "mp": 1495.0,
            "bp": 2870.0,
            "density": 8.9,
            "group": 9.0,
            "config": "[Ar] 3d7 4s2",
            "IE": 7.88
          },
          {
            "number": 28,
            "mass": 58.693,
            "name": "Nickel",
            "symbol": "Ni",
            "mp": 1453.0,
            "bp": 2732.0,
            "density": 8.9,
            "group": 10.0,
            "config": "[Ar] 3d8 4s2",
            "IE": 7.64
          },
          {
            "number": 29,
            "mass": 63.546,
            "name": "Copper",
            "symbol": "Cu",
            "mp": 1083.0,
            "bp": 2567.0,
            "density": 8.96,
            "group": 11.0,
            "config": "[Ar] 3d10 4s1",
            "IE": 7.73
          },
          {
            "number": 30,
            "mass": 65.39,
            "name": "Zinc",
            "symbol": "Zn",
            "mp": 420.0,
            "bp": 907.0,
            "density": 7.13,
            "group": 12.0,
            "config": "[Ar] 3d10 4s2",
            "IE": 9.39
          },
          {
            "number": 31,
            "mass": 69.723,
            "name": "Gallium",
            "symbol": "Ga",
            "mp": 30.0,
            "bp": 2403.0,
            "density": 5.91,
            "group": 13.0,
            "config": "[Ar] 3d10 4s2 4p1",
            "IE": 6.0
          },
          {
            "number": 32,
            "mass": 72.64,
            "name": "Germanium",
            "symbol": "Ge",
            "mp": 937.0,
            "bp": 2830.0,
            "density": 5.32,
            "group": 14.0,
            "config": "[Ar] 3d10 4s2 4p2",
            "IE": 7.9
          },
          {
            "number": 33,
            "mass": 74.922,
            "name": "Arsenic",
            "symbol": "As",
            "mp": 81.0,
            "bp": 613.0,
            "density": 5.72,
            "group": 15.0,
            "config": "[Ar] 3d10 4s2 4p3",
            "IE": 9.79
          },
          {
            "number": 34,
            "mass": 78.96,
            "name": "Selenium",
            "symbol": "Se",
            "mp": 217.0,
            "bp": 685.0,
            "density": 4.79,
            "group": 16.0,
            "config": "[Ar] 3d10 4s2 4p4",
            "IE": 9.75
          },
          {
            "number": 35,
            "mass": 79.904,
            "name": "Bromine",
            "symbol": "Br",
            "mp": -7.0,
            "bp": 59.0,
            "density": 3.12,
            "group": 17.0,
            "config": "[Ar] 3d10 4s2 4p5",
            "IE": 11.81
          },
          {
            "number": 36,
            "mass": 83.8,
            "name": "Krypton",
            "symbol": "Kr",
            "mp": -157.0,
            "bp": -153.0,
            "density": 3.75,
            "group": 18.0,
            "config": "[Ar] 3d10 4s2 4p6",
            "IE": 14.0
          },
          {
            "number": 37,
            "mass": 85.468,
            "name": "Rubidium",
            "symbol": "Rb",
            "mp": 39.0,
            "bp": 688.0,
            "density": 1.63,
            "group": 1.0,
            "config": "[Kr] 5s1",
            "IE": 4.18
          },
          {
            "number": 38,
            "mass": 87.62,
            "name": "Strontium",
            "symbol": "Sr",
            "mp": 769.0,
            "bp": 1384.0,
            "density": 2.54,
            "group": 2.0,
            "config": "[Kr] 5s2",
            "IE": 5.69
          },
          {
            "number": 39,
            "mass": 88.906,
            "name": "Yttrium",
            "symbol": "Y",
            "mp": 1523.0,
            "bp": 3337.0,
            "density": 4.47,
            "group": 3.0,
            "config": "[Kr] 4d1 5s2",
            "IE": 6.22
          },
          {
            "number": 40,
            "mass": 91.224,
            "name": "Zirconium",
            "symbol": "Zr",
            "mp": 1852.0,
            "bp": 4377.0,
            "density": 6.51,
            "group": 4.0,
            "config": "[Kr] 4d2 5s2",
            "IE": 6.63
          },
          {
            "number": 41,
            "mass": 92.906,
            "name": "Niobium",
            "symbol": "Nb",
            "mp": 2468.0,
            "bp": 4927.0,
            "density": 8.57,
            "group": 5.0,
            "config": "[Kr] 4d4 5s1",
            "IE": 6.76
          },
          {
            "number": 42,
            "mass": 95.94,
            "name": "Molybdenum",
            "symbol": "Mo",
            "mp": 2617.0,
            "bp": 4612.0,
            "density": 10.22,
            "group": 6.0,
            "config": "[Kr] 4d5 5s1",
            "IE": 7.09
          },
          {
            "number": 43,
            "mass": 98.0,
            "name": "Technetium",
            "symbol": "Tc",
            "mp": 2200.0,
            "bp": 4877.0,
            "density": 11.5,
            "group": 7.0,
            "config": "[Kr] 4d5 5s2",
            "IE": 7.28
          },
          {
            "number": 44,
            "mass": 101.07,
            "name": "Ruthenium",
            "symbol": "Ru",
            "mp": 2250.0,
            "bp": 3900.0,
            "density": 12.37,
            "group": 8.0,
            "config": "[Kr] 4d7 5s1",
            "IE": 7.36
          },
          {
            "number": 45,
            "mass": 102.906,
            "name": "Rhodium",
            "symbol": "Rh",
            "mp": 1966.0,
            "bp": 3727.0,
            "density": 12.41,
            "group": 9.0,
            "config": "[Kr] 4d8 5s1",
            "IE": 7.46
          },
          {
            "number": 46,
            "mass": 106.42,
            "name": "Palladium",
            "symbol": "Pd",
            "mp": 1552.0,
            "bp": 2927.0,
            "density": 12.02,
            "group": 10.0,
            "config": "[Kr] 4d10",
            "IE": 8.34
          },
          {
            "number": 47,
            "mass": 107.868,
            "name": "Silver",
            "symbol": "Ag",
            "mp": 962.0,
            "bp": 2212.0,
            "density": 10.5,
            "group": 11.0,
            "config": "[Kr] 4d10 5s1",
            "IE": 7.58
          },
          {
            "number": 48,
            "mass": 112.411,
            "name": "Cadmium",
            "symbol": "Cd",
            "mp": 321.0,
            "bp": 765.0,
            "density": 8.65,
            "group": 12.0,
            "config": "[Kr] 4d10 5s2",
            "IE": 8.99
          },
          {
            "number": 49,
            "mass": 114.818,
            "name": "Indium",
            "symbol": "In",
            "mp": 157.0,
            "bp": 2000.0,
            "density": 7.31,
            "group": 13.0,
            "config": "[Kr] 4d10 5s2 5p1",
            "IE": 5.79
          },
          {
            "number": 50,
            "mass": 118.71,
            "name": "Tin",
            "symbol": "Sn",
            "mp": 232.0,
            "bp": 2270.0,
            "density": 7.31,
            "group": 14.0,
            "config": "[Kr] 4d10 5s2 5p2",
            "IE": 7.34
          },
          {
            "number": 51,
            "mass": 121.76,
            "name": "Antimony",
            "symbol": "Sb",
            "mp": 630.0,
            "bp": 1750.0,
            "density": 6.68,
            "group": 15.0,
            "config": "[Kr] 4d10 5s2 5p3",
            "IE": 8.61
          },
          {
            "number": 52,
            "mass": 127.6,
            "name": "Tellurium",
            "symbol": "Te",
            "mp": 449.0,
            "bp": 990.0,
            "density": 6.24,
            "group": 16.0,
            "config": "[Kr] 4d10 5s2 5p4",
            "IE": 9.01
          },
          {
            "number": 53,
            "mass": 126.905,
            "name": "Iodine",
            "symbol": "I",
            "mp": 114.0,
            "bp": 184.0,
            "density": 4.93,
            "group": 17.0,
            "config": "[Kr] 4d10 5s2 5p5",
            "IE": 10.45
          },
          {
            "number": 54,
            "mass": 131.293,
            "name": "Xenon",
            "symbol": "Xe",
            "mp": -112.0,
            "bp": -108.0,
            "density": 5.9,
            "group": 18.0,
            "config": "[Kr] 4d10 5s2 5p6",
            "IE": 12.13
          },
          {
            "number": 55,
            "mass": 132.906,
            "name": "Cesium",
            "symbol": "Cs",
            "mp": 29.0,
            "bp": 678.0,
            "density": 1.87,
            "group": 1.0,
            "config": "[Xe] 6s1",
            "IE": 3.89
          },
          {
            "number": 56,
            "mass": 137.327,
            "name": "Barium",
            "symbol": "Ba",
            "mp": 725.0,
            "bp": 1140.0,
            "density": 3.59,
            "group": 2.0,
            "config": "[Xe] 6s2",
            "IE": 5.21
          },
          {
            "number": 57,
            "mass": 138.906,
            "name": "Lanthanum",
            "symbol": "La",
            "mp": 920.0,
            "bp": 3469.0,
            "density": 6.15,
            "group": 3.0,
            "config": "[Xe] 5d1 6s2",
            "IE": 5.58
          },
          {
            "number": 58,
            "mass": 140.116,
            "name": "Cerium",
            "symbol": "Ce",
            "mp": 795.0,
            "bp": 3257.0,
            "density": 6.77,
            "group": 101.0,
            "config": "[Xe] 4f1 5d1 6s2",
            "IE": 5.54
          },
          {
            "number": 59,
            "mass": 140.908,
            "name": "Praseodymium",
            "symbol": "Pr",
            "mp": 935.0,
            "bp": 3127.0,
            "density": 6.77,
            "group": 101.0,
            "config": "[Xe] 4f3 6s2",
            "IE": 5.47
          },
          {
            "number": 60,
            "mass": 144.24,
            "name": "Neodymium",
            "symbol": "Nd",
            "mp": 1010.0,
            "bp": 3127.0,
            "density": 7.01,
            "group": 101.0,
            "config": "[Xe] 4f4 6s2",
            "IE": 5.53
          },
          {
            "number": 61,
            "mass": 145.0,
            "name": "Promethium",
            "symbol": "Pm",
            "mp": 1100.0,
            "bp": 3000.0,
            "density": 7.3,
            "group": 101.0,
            "config": "[Xe] 4f5 6s2",
            "IE": 5.58
          },
          {
            "number": 62,
            "mass": 150.36,
            "name": "Samarium",
            "symbol": "Sm",
            "mp": 1072.0,
            "bp": 1900.0,
            "density": 7.52,
            "group": 101.0,
            "config": "[Xe] 4f6 6s2",
            "IE": 5.64
          },
          {
            "number": 63,
            "mass": 151.964,
            "name": "Europium",
            "symbol": "Eu",
            "mp": 822.0,
            "bp": 1597.0,
            "density": 5.24,
            "group": 101.0,
            "config": "[Xe] 4f7 6s2",
            "IE": 5.67
          },
          {
            "number": 64,
            "mass": 157.25,
            "name": "Gadolinium",
            "symbol": "Gd",
            "mp": 1311.0,
            "bp": 3233.0,
            "density": 7.9,
            "group": 101.0,
            "config": "[Xe] 4f7 5d1 6s2",
            "IE": 6.15
          },
          {
            "number": 65,
            "mass": 158.925,
            "name": "Terbium",
            "symbol": "Tb",
            "mp": 1360.0,
            "bp": 3041.0,
            "density": 8.23,
            "group": 101.0,
            "config": "[Xe] 4f9 6s2",
            "IE": 5.86
          },
          {
            "number": 66,
            "mass": 162.5,
            "name": "Dysprosium",
            "symbol": "Dy",
            "mp": 1412.0,
            "bp": 2562.0,
            "density": 8.55,
            "group": 101.0,
            "config": "[Xe] 4f10 6s2",
            "IE": 5.94
          },
          {
            "number": 67,
            "mass": 164.93,
            "name": "Holmium",
            "symbol": "Ho",
            "mp": 1470.0,
            "bp": 2720.0,
            "density": 8.8,
            "group": 101.0,
            "config": "[Xe] 4f11 6s2",
            "IE": 6.02
          },
          {
            "number": 68,
            "mass": 167.259,
            "name": "Erbium",
            "symbol": "Er",
            "mp": 1522.0,
            "bp": 2510.0,
            "density": 9.07,
            "group": 101.0,
            "config": "[Xe] 4f12 6s2",
            "IE": 6.11
          },
          {
            "number": 69,
            "mass": 168.934,
            "name": "Thulium",
            "symbol": "Tm",
            "mp": 1545.0,
            "bp": 1727.0,
            "density": 9.32,
            "group": 101.0,
            "config": "[Xe] 4f13 6s2",
            "IE": 6.18
          },
          {
            "number": 70,
            "mass": 173.04,
            "name": "Ytterbium",
            "symbol": "Yb",
            "mp": 824.0,
            "bp": 1466.0,
            "density": 6.9,
            "group": 101.0,
            "config": "[Xe] 4f14 6s2",
            "IE": 6.25
          },
          {
            "number": 71,
            "mass": 174.967,
            "name": "Lutetium",
            "symbol": "Lu",
            "mp": 1656.0,
            "bp": 3315.0,
            "density": 9.84,
            "group": 101.0,
            "config": "[Xe] 4f14 5d1 6s2",
            "IE": 5.43
          },
          {
            "number": 72,
            "mass": 178.49,
            "name": "Hafnium",
            "symbol": "Hf",
            "mp": 2150.0,
            "bp": 5400.0,
            "density": 13.31,
            "group": 4.0,
            "config": "[Xe] 4f14 5d2 6s2",
            "IE": 6.83
          },
          {
            "number": 73,
            "mass": 180.948,
            "name": "Tantalum",
            "symbol": "Ta",
            "mp": 2996.0,
            "bp": 5425.0,
            "density": 16.65,
            "group": 5.0,
            "config": "[Xe] 4f14 5d3 6s2",
            "IE": 7.55
          },
          {
            "number": 74,
            "mass": 183.84,
            "name": "Tungsten",
            "symbol": "W",
            "mp": 3410.0,
            "bp": 5660.0,
            "density": 19.35,
            "group": 6.0,
            "config": "[Xe] 4f14 5d4 6s2",
            "IE": 7.86
          },
          {
            "number": 75,
            "mass": 186.207,
            "name": "Rhenium",
            "symbol": "Re",
            "mp": 3180.0,
            "bp": 5627.0,
            "density": 21.04,
            "group": 7.0,
            "config": "[Xe] 4f14 5d5 6s2",
            "IE": 7.83
          },
          {
            "number": 76,
            "mass": 190.23,
            "name": "Osmium",
            "symbol": "Os",
            "mp": 3045.0,
            "bp": 5027.0,
            "density": 22.6,
            "group": 8.0,
            "config": "[Xe] 4f14 5d6 6s2",
            "IE": 8.44
          },
          {
            "number": 77,
            "mass": 192.217,
            "name": "Iridium",
            "symbol": "Ir",
            "mp": 2410.0,
            "bp": 4527.0,
            "density": 22.4,
            "group": 9.0,
            "config": "[Xe] 4f14 5d7 6s2",
            "IE": 8.97
          },
          {
            "number": 78,
            "mass": 195.078,
            "name": "Platinum",
            "symbol": "Pt",
            "mp": 1772.0,
            "bp": 3827.0,
            "density": 21.45,
            "group": 10.0,
            "config": "[Xe] 4f14 5d9 6s1",
            "IE": 8.96
          },
          {
            "number": 79,
            "mass": 196.967,
            "name": "Gold",
            "symbol": "Au",
            "mp": 1064.0,
            "bp": 2807.0,
            "density": 19.32,
            "group": 11.0,
            "config": "[Xe] 4f14 5d10 6s1",
            "IE": 9.23
          },
          {
            "number": 80,
            "mass": 200.59,
            "name": "Mercury",
            "symbol": "Hg",
            "mp": -39.0,
            "bp": 357.0,
            "density": 13.55,
            "group": 12.0,
            "config": "[Xe] 4f14 5d10 6s2",
            "IE": 10.44
          },
          {
            "number": 81,
            "mass": 204.383,
            "name": "Thallium",
            "symbol": "Tl",
            "mp": 303.0,
            "bp": 1457.0,
            "density": 11.85,
            "group": 13.0,
            "config": "[Xe] 4f14 5d10 6s2 6p1",
            "IE": 6.11
          },
          {
            "number": 82,
            "mass": 207.2,
            "name": "Lead",
            "symbol": "Pb",
            "mp": 327.0,
            "bp": 1740.0,
            "density": 11.35,
            "group": 14.0,
            "config": "[Xe] 4f14 5d10 6s2 6p2",
            "IE": 7.42
          },
          {
            "number": 83,
            "mass": 208.98,
            "name": "Bismuth",
            "symbol": "Bi",
            "mp": 271.0,
            "bp": 1560.0,
            "density": 9.75,
            "group": 15.0,
            "config": "[Xe] 4f14 5d10 6s2 6p3",
            "IE": 7.29
          },
          {
            "number": 84,
            "mass": 209.0,
            "name": "Polonium",
            "symbol": "Po",
            "mp": 254.0,
            "bp": 962.0,
            "density": 9.3,
            "group": 16.0,
            "config": "[Xe] 4f14 5d10 6s2 6p4",
            "IE": 8.42
          },
          {
            "number": 85,
            "mass": 210.0,
            "name": "Astatine",
            "symbol": "At",
            "mp": 302.0,
            "bp": 337.0,
            "density": 0.0,
            "group": 17.0,
            "config": "[Xe] 4f14 5d10 6s2 6p5",
            "IE": 9.3
          },
          {
            "number": 86,
            "mass": 222.0,
            "name": "Radon",
            "symbol": "Rn",
            "mp": -71.0,
            "bp": -62.0,
            "density": 9.73,
            "group": 18.0,
            "config": "[Xe] 4f14 5d10 6s2 6p6",
            "IE": 10.75
          },
          {
            "number": 87,
            "mass": 223.0,
            "name": "Francium",
            "symbol": "Fr",
            "mp": 27.0,
            "bp": 677.0,
            "density": 0.0,
            "group": 1.0,
            "config": "[Rn] 7s1",
            "IE": 4.07
          },
          {
            "number": 88,
            "mass": 226.0,
            "name": "Radium",
            "symbol": "Ra",
            "mp": 700.0,
            "bp": 1737.0,
            "density": 5.5,
            "group": 2.0,
            "config": "[Rn] 7s2",
            "IE": 5.28
          },
          {
            "number": 89,
            "mass": 227.0,
            "name": "Actinium",
            "symbol": "Ac",
            "mp": 1050.0,
            "bp": 3200.0,
            "density": 10.07,
            "group": 3.0,
            "config": "[Rn] 6d1 7s2",
            "IE": 5.17
          },
          {
            "number": 90,
            "mass": 232.038,
            "name": "Thorium",
            "symbol": "Th",
            "mp": 1750.0,
            "bp": 4790.0,
            "density": 11.72,
            "group": 102.0,
            "config": "[Rn] 6d2 7s2",
            "IE": 6.31
          },
          {
            "number": 91,
            "mass": 231.036,
            "name": "Protactinium",
            "symbol": "Pa",
            "mp": 1568.0,
            "bp": 0.0,
            "density": 15.4,
            "group": 102.0,
            "config": "[Rn] 5f2 6d1 7s2",
            "IE": 5.89
          },
          {
            "number": 92,
            "mass": 238.029,
            "name": "Uranium",
            "symbol": "U",
            "mp": 1132.0,
            "bp": 3818.0,
            "density": 18.95,
            "group": 102.0,
            "config": "[Rn] 5f3 6d1 7s2",
            "IE": 6.19
          },
          {
            "number": 93,
            "mass": 237.0,
            "name": "Neptunium",
            "symbol": "Np",
            "mp": 640.0,
            "bp": 3902.0,
            "density": 20.2,
            "group": 102.0,
            "config": "[Rn] 5f4 6d1 7s2",
            "IE": 6.27
          },
          {
            "number": 94,
            "mass": 244.0,
            "name": "Plutonium",
            "symbol": "Pu",
            "mp": 640.0,
            "bp": 3235.0,
            "density": 19.84,
            "group": 102.0,
            "config": "[Rn] 5f6 7s2",
            "IE": 6.03
          },
          {
            "number": 95,
            "mass": 243.0,
            "name": "Americium",
            "symbol": "Am",
            "mp": 994.0,
            "bp": 2607.0,
            "density": 13.67,
            "group": 102.0,
            "config": "[Rn] 5f7 7s2",
            "IE": 5.97
          },
          {
            "number": 96,
            "mass": 247.0,
            "name": "Curium",
            "symbol": "Cm",
            "mp": 1340.0,
            "bp": 0.0,
            "density": 13.5,
            "group": 102.0,
            "config": "",
            "IE": 5.99
          },
          {
            "number": 97,
            "mass": 247.0,
            "name": "Berkelium",
            "symbol": "Bk",
            "mp": 986.0,
            "bp": 0.0,
            "density": 14.78,
            "group": 102.0,
            "config": "",
            "IE": 6.2
          },
          {
            "number": 98,
            "mass": 251.0,
            "name": "Californium",
            "symbol": "Cf",
            "mp": 900.0,
            "bp": 0.0,
            "density": 15.1,
            "group": 102.0,
            "config": "",
            "IE": 6.28
          },
          {
            "number": 99,
            "mass": 252.0,
            "name": "Einsteinium",
            "symbol": "Es",
            "mp": 860.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 102.0,
            "config": "",
            "IE": 6.42
          },
          {
            "number": 100,
            "mass": 257.0,
            "name": "Fermium",
            "symbol": "Fm",
            "mp": 1527.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 102.0,
            "config": "",
            "IE": 6.5
          },
          {
            "number": 101,
            "mass": 258.0,
            "name": "Mendelevium",
            "symbol": "Md",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 102.0,
            "config": "",
            "IE": 6.58
          },
          {
            "number": 102,
            "mass": 259.0,
            "name": "Nobelium",
            "symbol": "No",
            "mp": 827.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 102.0,
            "config": "",
            "IE": 6.65
          },
          {
            "number": 103,
            "mass": 262.0,
            "name": "Lawrencium",
            "symbol": "Lr",
            "mp": 1627.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 102.0,
            "config": "",
            "IE": 4.9
          },
          {
            "number": 104,
            "mass": 261.0,
            "name": "Rutherfordium",
            "symbol": "Rf",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 4.0,
            "config": "",
            "IE": 0.0
          },
          {
            "number": 105,
            "mass": 262.0,
            "name": "Dubnium",
            "symbol": "Db",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 5.0,
            "config": "",
            "IE": 0.0
          },
          {
            "number": 106,
            "mass": 266.0,
            "name": "Seaborgium",
            "symbol": "Sg",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 6.0,
            "config": "",
            "IE": 0.0
          },
          {
            "number": 107,
            "mass": 264.0,
            "name": "Bohrium",
            "symbol": "Bh",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 7.0,
            "config": "",
            "IE": 0.0
          },
          {
            "number": 108,
            "mass": 277.0,
            "name": "Hassium",
            "symbol": "Hs",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 8.0,
            "config": "",
            "IE": 0.0
          },
          {
            "number": 109,
            "mass": 268.0,
            "name": "Meitnerium",
            "symbol": "Mt",
            "mp": 0.0,
            "bp": 0.0,
            "density": 0.0,
            "group": 9.0,
            "config": "",
            "IE": 0.0
          }
        ]

        self.ui = Ui_ClusterID()
        self.ui.setupUi(self)

        self.setWindowTitle("ClusterID v1")
        self.setWindowIcon(QIcon(':cluster.ico'))

        self.periodicTable = {}
        self.selectedElements = []
        self.matchedClusters = []
        self.targetVal = 217
        self.clusterSeriesDicts = []
        self.formattedMatchOutput = ''
        self.formattedSeriesOutput = ''
        self.absoluteTolerance = 1
        self.maxClusterAtoms = 10

        for element in self.elements:
            self.periodicTable[element['symbol']] = Element(element['mass'], element['symbol'], element['name'], element['number'])

        # Button that initiates the matching algorithm
        self.ui.btnFindMatches.clicked.connect(self.handleFindMatches)
        self.ui.btnFindClusterSeries.clicked.connect(self.handleFindClusterSeries)

        # Line edit that sets the target mass
        self.ui.targetLineEdit.textChanged[str].connect(self.updateTarget)
        self.ui.targetLineEdit.returnPressed.connect(self.handleFindMatches)

        # Checkbox that toggles sort by mass for cluster series
        self.ui.checkSortByMass.clicked[bool].connect(self.toggleSortByMass)

        # Filter line edit for the cluster series
        self.ui.filterClusterSeries.textChanged.connect(self.handleFilter)
        self.ui.filterClusterSeries.returnPressed.connect(self.handleFilter)

        # Allows user to set the max single atom number to generate cluster
        # series for
        self.ui.maxAtomsLineEdit.setText(str(self.maxClusterAtoms))
        self.ui.maxAtomsLineEdit.textChanged[str].connect(self.updateMaxAtoms)

        # Allows user to set the absolute tolerance for returned matches
        # (how many amu from target)
        self.ui.toleranceLineEdit.setText(str(self.absoluteTolerance))
        self.ui.toleranceLineEdit.textChanged[str].connect(self.updateTolerance)

        # Tried for an unreasonable amount of time to use findChildren to
        # iterate over the UI buttons to assign signal/slots, but to no avail
        self.ui.btnH.clicked[bool].connect(self.elementClicked)
        self.ui.btnLi.clicked[bool].connect(self.elementClicked)
        self.ui.btnNa.clicked[bool].connect(self.elementClicked)
        self.ui.btnRb.clicked[bool].connect(self.elementClicked)
        self.ui.btnK.clicked[bool].connect(self.elementClicked)
        self.ui.btnCs.clicked[bool].connect(self.elementClicked)
        self.ui.btnFr.clicked[bool].connect(self.elementClicked)
        self.ui.btnCa.clicked[bool].connect(self.elementClicked)
        self.ui.btnRa.clicked[bool].connect(self.elementClicked)
        self.ui.btnBe.clicked[bool].connect(self.elementClicked)
        self.ui.btnSr.clicked[bool].connect(self.elementClicked)
        self.ui.btnBa.clicked[bool].connect(self.elementClicked)
        self.ui.btnMg.clicked[bool].connect(self.elementClicked)
        self.ui.btnSc.clicked[bool].connect(self.elementClicked)
        self.ui.btnTi.clicked[bool].connect(self.elementClicked)
        self.ui.btnV.clicked[bool].connect(self.elementClicked)
        self.ui.btnFe.clicked[bool].connect(self.elementClicked)
        self.ui.btnMn.clicked[bool].connect(self.elementClicked)
        self.ui.btnCr.clicked[bool].connect(self.elementClicked)
        self.ui.btnZn.clicked[bool].connect(self.elementClicked)
        self.ui.btnNi.clicked[bool].connect(self.elementClicked)
        self.ui.btnCo.clicked[bool].connect(self.elementClicked)
        self.ui.btnCu.clicked[bool].connect(self.elementClicked)
        self.ui.btnZr.clicked[bool].connect(self.elementClicked)
        self.ui.btnRh.clicked[bool].connect(self.elementClicked)
        self.ui.btnPd.clicked[bool].connect(self.elementClicked)
        self.ui.btnY.clicked[bool].connect(self.elementClicked)
        self.ui.btnAg.clicked[bool].connect(self.elementClicked)
        self.ui.btnRu.clicked[bool].connect(self.elementClicked)
        self.ui.btnNb.clicked[bool].connect(self.elementClicked)
        self.ui.btnMo.clicked[bool].connect(self.elementClicked)
        self.ui.btnTc.clicked[bool].connect(self.elementClicked)
        self.ui.btnCd.clicked[bool].connect(self.elementClicked)
        self.ui.btnIn.clicked[bool].connect(self.elementClicked)
        self.ui.btnGa.clicked[bool].connect(self.elementClicked)
        self.ui.btnTl.clicked[bool].connect(self.elementClicked)
        self.ui.btnAl.clicked[bool].connect(self.elementClicked)
        self.ui.btnB.clicked[bool].connect(self.elementClicked)
        self.ui.btnC.clicked[bool].connect(self.elementClicked)
        self.ui.btnGe.clicked[bool].connect(self.elementClicked)
        self.ui.btnPb.clicked[bool].connect(self.elementClicked)
        self.ui.btnSi.clicked[bool].connect(self.elementClicked)
        self.ui.btnSn.clicked[bool].connect(self.elementClicked)
        self.ui.btnN.clicked[bool].connect(self.elementClicked)
        self.ui.btnAs.clicked[bool].connect(self.elementClicked)
        self.ui.btnTe.clicked[bool].connect(self.elementClicked)
        self.ui.btnS.clicked[bool].connect(self.elementClicked)
        self.ui.btnBi.clicked[bool].connect(self.elementClicked)
        self.ui.btnP.clicked[bool].connect(self.elementClicked)
        self.ui.btnSe.clicked[bool].connect(self.elementClicked)
        self.ui.btnPo.clicked[bool].connect(self.elementClicked)
        self.ui.btnO.clicked[bool].connect(self.elementClicked)
        self.ui.btnSb.clicked[bool].connect(self.elementClicked)
        self.ui.btnF.clicked[bool].connect(self.elementClicked)
        self.ui.btnBr.clicked[bool].connect(self.elementClicked)
        self.ui.btnXe.clicked[bool].connect(self.elementClicked)
        self.ui.btnAr.clicked[bool].connect(self.elementClicked)
        self.ui.btnAt.clicked[bool].connect(self.elementClicked)
        self.ui.btnCl.clicked[bool].connect(self.elementClicked)
        self.ui.btnKr.clicked[bool].connect(self.elementClicked)
        self.ui.btnRn.clicked[bool].connect(self.elementClicked)
        self.ui.btnNe.clicked[bool].connect(self.elementClicked)
        self.ui.btnI.clicked[bool].connect(self.elementClicked)
        self.ui.btnHe.clicked[bool].connect(self.elementClicked)
        self.ui.btnBh.clicked[bool].connect(self.elementClicked)
        self.ui.btnOs.clicked[bool].connect(self.elementClicked)
        self.ui.btnDb.clicked[bool].connect(self.elementClicked)
        self.ui.btnHf.clicked[bool].connect(self.elementClicked)
        self.ui.btnTa.clicked[bool].connect(self.elementClicked)
        self.ui.btnPt.clicked[bool].connect(self.elementClicked)
        self.ui.btnMt.clicked[bool].connect(self.elementClicked)
        self.ui.btnAu.clicked[bool].connect(self.elementClicked)
        self.ui.btnRe.clicked[bool].connect(self.elementClicked)
        self.ui.btnW.clicked[bool].connect(self.elementClicked)
        self.ui.btnSg.clicked[bool].connect(self.elementClicked)
        self.ui.btnRf.clicked[bool].connect(self.elementClicked)
        self.ui.btnHg.clicked[bool].connect(self.elementClicked)
        self.ui.btnIr.clicked[bool].connect(self.elementClicked)
        self.ui.btnHs.clicked[bool].connect(self.elementClicked)
        self.ui.btnNp.clicked[bool].connect(self.elementClicked)
        self.ui.btnSm.clicked[bool].connect(self.elementClicked)
        self.ui.btnPa.clicked[bool].connect(self.elementClicked)
        self.ui.btnBk.clicked[bool].connect(self.elementClicked)
        self.ui.btnCm.clicked[bool].connect(self.elementClicked)
        self.ui.btnCe.clicked[bool].connect(self.elementClicked)
        self.ui.btnPr.clicked[bool].connect(self.elementClicked)
        self.ui.btnGd.clicked[bool].connect(self.elementClicked)
        self.ui.btnAm.clicked[bool].connect(self.elementClicked)
        self.ui.btnTb.clicked[bool].connect(self.elementClicked)
        self.ui.btnPm.clicked[bool].connect(self.elementClicked)
        self.ui.btnNd.clicked[bool].connect(self.elementClicked)
        self.ui.btnU.clicked[bool].connect(self.elementClicked)
        self.ui.btnCf.clicked[bool].connect(self.elementClicked)
        self.ui.btnTh.clicked[bool].connect(self.elementClicked)
        self.ui.btnDy.clicked[bool].connect(self.elementClicked)
        self.ui.btnAc.clicked[bool].connect(self.elementClicked)
        self.ui.btnEu.clicked[bool].connect(self.elementClicked)
        self.ui.btnLa.clicked[bool].connect(self.elementClicked)
        self.ui.btnPu.clicked[bool].connect(self.elementClicked)
        self.ui.btnFm.clicked[bool].connect(self.elementClicked)
        self.ui.btnEs.clicked[bool].connect(self.elementClicked)
        self.ui.btnLr.clicked[bool].connect(self.elementClicked)
        self.ui.btnNo.clicked[bool].connect(self.elementClicked)
        self.ui.btnHo.clicked[bool].connect(self.elementClicked)
        self.ui.btnTm.clicked[bool].connect(self.elementClicked)
        self.ui.btnEr.clicked[bool].connect(self.elementClicked)
        self.ui.btnMd.clicked[bool].connect(self.elementClicked)
        self.ui.btnLu.clicked[bool].connect(self.elementClicked)
        self.ui.btnYb.clicked[bool].connect(self.elementClicked)

    # Adds or removes clicked element from selected elements list
    def elementClicked(self, checked):
        elementObject = self.periodicTable[self.sender().text()]
        mass = self.periodicTable[self.sender().text()].mass
        symbol = self.periodicTable[self.sender().text()].symbol
        if checked and elementObject not in self.selectedElements:
            self.selectedElements.append(elementObject)
        elif not checked:
            self.selectedElements.remove(elementObject)
        #print(self.selectedElements)

    # Updates target mass when line edit value changes
    def updateTarget(self, value):
        if value.isdigit():
            self.targetVal = float(value)

    # Updates max atoms per element in cluster series when line edit value changes
    def updateMaxAtoms(self, value):
        if value.isdigit():
            self.maxClusterAtoms = int(value)

    # Updates absolute tolerance when line edit value changes
    def updateTolerance(self, value):
        if value.isdigit():
            self.absoluteTolerance = float(value)

    # Finds all possible ways to partition the target value
    # with the values contained in a list.
    # Recursively finds each combination by incrementing last value in list by +1 until no remainder,
    # then increments the second to last by +1, etc.
    def recursiveFindCombinations(self, target, numList, depth=0, combination=[], answer=set()):
      if numList != []:
        maxIons = int(target // numList[0]) + 1

        # Adds an additional multiple of the current value for each iteration
        for i in range(0, maxIons + 1):

          # Most target values will be integers. This allows for some tolerance between precise atomic
          # masses and imprecise target value
          # if math.isclose(target, numList[0] * i, abs_tol=1):
          if abs(target - numList[0] * i) <= self.absoluteTolerance:
            remainder = 0
          else:
            remainder = target - (numList[0] * i)
          combination[depth] = i

          # Terminating case: when the target is matched, combo list is copied
          if numList[1:] == [] and remainder == 0:
            answer.add(tuple(combination[:]))
          #print('n:', numList[0], 'maxIons:', maxIons, 'i:', i, 'total:', i * numList[0], 'remainder:', remainder, 'numList:', numList[1:], 'combo:', combination, 'answer:', answer)

          # Recursion: calls the function for the next value in numList
          self.recursiveFindCombinations(remainder, numList[1:], depth + 1, combination, answer=answer)
      return answer

    # Finds the precise mass of the match, used to calculate % difference
    def findPreciseMass(self, combination, includeList):
      total = 0
      for i in range(len(combination)):
        total = total + combination[i] * includeList[i]
      return total

    def findPercentDifference(self, valOne, valTwo):
        return abs((valOne - valTwo)/((valOne + valTwo)/2) * 100)

    # Used by both cluster series and matches to setText of appropriate text box
    def displayFormattedOutput(self, uiObject, outputString):
        uiObject.setHtml(outputString)

    # Function that formats the string to be returned for the find matches functionality
    def showMatches(self, elementObjects, matchList):
        if matchList == []:
            outputString = 'No Matches Found!'
        else:
            outputString = ''
            for match in matchList:
                matchString = ''
                for i in range(len(match['part'])):
                    if match['part'][i]:
                        matchString = matchString + '<a href="www.google.com">' + elementObjects[i].symbol + '<sub>' + str(match['part'][i]) + '</sub>'
                matchString = matchString + ', ' + str(round(match['preciseMass'], 5)) + ', ' + str(round(match['pctDif'], 5)) + '%</a><br/>'
                outputString = outputString + matchString
        print(outputString)

        self.formattedMatchOutput = outputString
        #print(self.formattedMatchOutput)
        self.displayFormattedOutput(self.ui.matchOutput, outputString)

    # Finds total number of unique elements in a match, used to sort returned matches
    def findNumberOfElements(self, combination):
        totalUniqueElements = 0
        for i in combination:
            if i:
                totalUniqueElements += 1
        return totalUniqueElements

    def handleFindMatches(self):
        # Find elemental masses for element list populated by pushbuttons
        sortedElementObjects = sorted(self.selectedElements, key=attrgetter('mass'), reverse=True)
        #for element in self.selectedElements:
            #selectedMasses.append(self.periodicTable[element].mass)

        # Sort masses highest to lowest
        #sortedMasses = sorted(selectedMasses, reverse=True)
        # Create template of 0s for 'combinations' list used in recursive function
        sortedMasses = [element.mass for element in sortedElementObjects]
        combinationTemplate = [0 for i in sortedMasses]

        # Call to recursive function, needs answer=set() to avoid
        # unwanted mutation
        allanswers = self.recursiveFindCombinations(self.targetVal, sortedMasses, combination=combinationTemplate, answer=set())

        # Sort answers by total atoms
        sortedallanswers = sorted(allanswers, key=sum)
        #print(sortedallanswers)

        # Create list of dicts and populate with first 20 answers (by lowest
        # total atoms), pct dif from target, and precise mass
        answerDicts = []
        for answer in sortedallanswers[:19]:
            preciseMass = self.findPreciseMass(answer, sortedMasses)
            pctDif = self.findPercentDifference(preciseMass, self.targetVal)
            answerDict = {}
            answerDict['part'] = answer
            answerDict['pctDif'] = pctDif
            answerDict['preciseMass'] = preciseMass
            answerDict['uniqueElements'] = self.findNumberOfElements(answer)
            answerDict['atomSum'] = sum(answer)
            answerDicts.append(answerDict)

        # Sort answer dict by percent difference from target
        sortedPctDiftAnswers = sorted(answerDicts, key=itemgetter('pctDif'))

        # Sort by number of unique elements, then total number of atoms
        sortedUniqueElementsAndSum = sorted(answerDicts, key=itemgetter('atomSum', 'uniqueElements'))

        #print(sortedUniqueElementsAndSum)
        self.matchedClusters = sortedUniqueElementsAndSum

        self.showMatches(sortedElementObjects, self.matchedClusters)

    # Recursive function used to find all combinations of included elements
    # up to a certain value, returns set of tuples
    def findClusterSeries(self, elementObjects, maxSize, combination=[], depth=0, output=set()):
        if elementObjects != []:
            for i in range(1, maxSize + 1):
                combination[depth] = i
                #print('i:', i, 'depth:', depth, 'combo:', combination, output)
                if elementObjects[1:] == []:
                    output.add(tuple(combination[:]))
                else:
                    self.findClusterSeries(elementObjects[1:], maxSize, combination, depth + 1, output)
        return output

    # Function that handles string formatting of cluster series and assignment
    # of QTextEdit value to formatted string
    def showCombinations(self, elementObjects, combinationDicts):
        outputString = ''
        if combinationDicts == []:
            outputString = 'Select a set of Elements.'
        else:
            for combinationDict in combinationDicts:
                formulaString = ''
                for i in range(len(combinationDict['combination'])):
                    if combinationDict['combination'][i] != 0:
                        formulaString = formulaString + elementObjects[i].symbol + '<sub>' + str(combinationDict['combination'][i]) + '</sub>'
                outputString = outputString + formulaString + ', ' + str(combinationDict['mass']) + '<br/>'
        #print(outputString)
        self.formattedSeriesOutput = outputString
        #print(self.formattedSeriesOutput)
        self.displayFormattedOutput(self.ui.seriesOutput, outputString)

    def handleFindClusterSeries(self):
        sortedElementObjects = sorted(self.selectedElements, key=attrgetter('mass'), reverse=True)
        #print(sortedElementObjects)
        # Needs output=set() to avoid unwanted mutation
        combinationsList = self.findClusterSeries(sortedElementObjects, self.maxClusterAtoms, [0 for i in sortedElementObjects], output=set())
        #print(combinationsList)
        sortedCombinationsList = sorted(combinationsList)
        #print(sortedCombinationsList)

        combinationDicts = []
        for combination in sortedCombinationsList:
            totalMass = 0
            #print(combination)
            for i in range(len(combination)):
                totalMass = totalMass + combination[i] * sortedElementObjects[i].mass
            combinationDict = {'combination': combination, 'mass': round(totalMass, 5)}
            combinationDicts.append(combinationDict)
        if not self.ui.checkSortByMass.isChecked():
            self.clusterSeriesDicts = combinationDicts
        else:
            self.clusterSeriesDicts = sorted(combinationDicts, key=itemgetter('mass'))
        self.lastRunClusterElements = sortedElementObjects

        self.showCombinations(sortedElementObjects, self.clusterSeriesDicts)

    # Function called by checking 'sort by mass' QCheckBox
    # Checks for stored clusterseriesdicts and value of box, sorts, and reshows
    # combinations
    def toggleSortByMass(self, bool):
        if bool and self.clusterSeriesDicts:
            sortedClusterSeriesMass = sorted(self.clusterSeriesDicts, key=itemgetter('mass'))
            self.showCombinations(self.lastRunClusterElements, sortedClusterSeriesMass)
        elif not bool and self.clusterSeriesDicts:
            sortedClusterSeriesAtoms = sorted(self.clusterSeriesDicts, key=itemgetter('combination'))
            self.showCombinations(self.lastRunClusterElements, sortedClusterSeriesAtoms)

    def constructRegex(self, filterStr):
      # Template: '(?:\w+<sub>\d+<\/sub>)*(?:\w+<sub>\d+<\/sub>)(?:\w+<sub>\d+<\/sub>)*,\s\d+\D*\d+<br\/>'
      splitFilterStr = list(filterStr.strip())
      concatList = []
      previousType = None
      concatVal = ''
      for i, val in enumerate(filterStr):
        #print(i, val)
        currentType = val.isdigit()
        #print(currentType)
        if currentType == previousType or previousType == None:
          concatVal += str(val)
          previousType = currentType
          #print(concatVal)
        else:
          concatList.append(concatVal)
          concatVal = val
          previousType = currentType
      concatList.append(concatVal)

      regexFormula = ''
      for i, entry in enumerate(concatList):
        if i % 2 == 0:
          if i == len(concatList) - 1:
              # Empty filter string constructs regex to return all
              if entry == '':
                  regexFormula += ''
              # Inserts atomic symbol into regex (e.g. '(?:V<sub>\d+<\/sub>)')
              # Case where filterStr terminates with atomic symbol, not number:
              else:
                  regexFormula += '(?:' + entry + '<sub>\d+<\/sub>)'
          # Inserts atomic symbol into regex (e.g. '(?:V<sub>\d+<\/sub>)')
          else:
              regexFormula += '(?:' + entry
        # Inserts number into regex (e.g. '(?:V<sub>3<\/sub>)')
        elif i % 2 != 0:
            regexFormula += '<sub>' + entry + '<\/sub>)'

      outputRegexStr = '(?:\w+<sub>\d+<\/sub>)*' + regexFormula + '(?:\w+<sub>\d+<\/sub>)*,\s\d+\D*\d+<br\/>'
      return outputRegexStr

    def handleFilter(self):
      filterStr = self.ui.filterClusterSeries.text()
      testStr = self.formattedSeriesOutput

      filteredEntries = set()
      try:
        float(filterStr)
      except ValueError:
        regexStr = self.constructRegex(filterStr)
        #print(regexStr)
        result = re.findall(regexStr, testStr)
        joinedFilteredEntries = ''.join(result)
        #print(joinedFilteredEntries)
        #self.formattedSeriesOutput = joinedFilteredEntries
        self.displayFormattedOutput(self.ui.seriesOutput, joinedFilteredEntries)
      else:
        splitStr = testStr.split('<br/>')
        for clusterEntry in splitStr:
          if filterStr.strip() in clusterEntry:
            filteredEntries.add(clusterEntry)
        joinedFilteredEntries = '<br/>'.join(filteredEntries)
        #self.formattedSeriesOutput = joinedFilteredEntries
        #print(filteredEntries)
        self.displayFormattedOutput(self.ui.seriesOutput, joinedFilteredEntries)

if __name__ =='__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
