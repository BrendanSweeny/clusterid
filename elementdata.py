class ElementData:
    def __init__(self):
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
        self.isotopes = [
          {
            "symbol": "H",
            "isotopes": [
              [
                1,
                99.9885
              ],
              [
                2,
                0.0115
              ]
            ]
          },
          {
            "symbol": "He",
            "isotopes": [
              [
                3,
                0.000137
              ],
              [
                4,
                99.999863
              ]
            ]
          },
          {
            "symbol": "Li",
            "isotopes": [
              [
                6,
                7.59
              ],
              [
                7,
                92.41
              ]
            ]
          },
          {
            "symbol": "Be",
            "isotopes": [
              [
                9,
                100.0
              ]
            ]
          },
          {
            "symbol": "B",
            "isotopes": [
              [
                10,
                19.9
              ],
              [
                11,
                80.1
              ]
            ]
          },
          {
            "symbol": "C",
            "isotopes": [
              [
                12,
                98.93
              ],
              [
                13,
                1.07
              ]
            ]
          },
          {
            "symbol": "N",
            "isotopes": [
              [
                14,
                99.632
              ],
              [
                15,
                0.368
              ]
            ]
          },
          {
            "symbol": "O",
            "isotopes": [
              [
                16,
                99.757
              ],
              [
                17,
                0.038
              ],
              [
                18,
                0.205
              ]
            ]
          },
          {
            "symbol": "F",
            "isotopes": [
              [
                19,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ne",
            "isotopes": [
              [
                20,
                90.48
              ],
              [
                21,
                0.27
              ],
              [
                22,
                9.25
              ]
            ]
          },
          {
            "symbol": "Na",
            "isotopes": [
              [
                23,
                100.0
              ]
            ]
          },
          {
            "symbol": "Mg",
            "isotopes": [
              [
                24,
                78.99
              ],
              [
                25,
                10.0
              ],
              [
                26,
                11.01
              ]
            ]
          },
          {
            "symbol": "Al",
            "isotopes": [
              [
                27,
                100.0
              ]
            ]
          },
          {
            "symbol": "Si",
            "isotopes": [
              [
                28,
                92.2297
              ],
              [
                29,
                4.6832
              ],
              [
                30,
                3.0872
              ]
            ]
          },
          {
            "symbol": "P",
            "isotopes": [
              [
                31,
                100.0
              ]
            ]
          },
          {
            "symbol": "S",
            "isotopes": [
              [
                32,
                94.93
              ],
              [
                33,
                0.76
              ],
              [
                34,
                4.29
              ],
              [
                36,
                0.02
              ]
            ]
          },
          {
            "symbol": "Cl",
            "isotopes": [
              [
                35,
                75.78
              ],
              [
                37,
                24.22
              ]
            ]
          },
          {
            "symbol": "Ar",
            "isotopes": [
              [
                36,
                0.3365
              ],
              [
                38,
                0.0632
              ],
              [
                40,
                99.6003
              ]
            ]
          },
          {
            "symbol": "K",
            "isotopes": [
              [
                39,
                93.2581
              ],
              [
                40,
                0.0117
              ],
              [
                41,
                6.7302
              ]
            ]
          },
          {
            "symbol": "Ca",
            "isotopes": [
              [
                40,
                96.941
              ],
              [
                42,
                0.647
              ],
              [
                43,
                0.135
              ],
              [
                44,
                2.086
              ],
              [
                46,
                0.004
              ],
              [
                48,
                0.187
              ]
            ]
          },
          {
            "symbol": "Sc",
            "isotopes": [
              [
                45,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ti",
            "isotopes": [
              [
                46,
                8.25
              ],
              [
                47,
                7.44
              ],
              [
                48,
                73.72
              ],
              [
                49,
                5.41
              ],
              [
                50,
                5.18
              ]
            ]
          },
          {
            "symbol": "V",
            "isotopes": [
              [
                50,
                0.25
              ],
              [
                51,
                99.75
              ]
            ]
          },
          {
            "symbol": "Cr",
            "isotopes": [
              [
                50,
                4.345
              ],
              [
                52,
                83.789
              ],
              [
                53,
                9.501
              ],
              [
                54,
                2.365
              ]
            ]
          },
          {
            "symbol": "Mn",
            "isotopes": [
              [
                55,
                100.0
              ]
            ]
          },
          {
            "symbol": "Fe",
            "isotopes": [
              [
                54,
                5.845
              ],
              [
                56,
                91.754
              ],
              [
                57,
                2.119
              ],
              [
                58,
                0.282
              ]
            ]
          },
          {
            "symbol": "Co",
            "isotopes": [
              [
                59,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ni",
            "isotopes": [
              [
                58,
                68.0769
              ],
              [
                60,
                26.2231
              ],
              [
                61,
                1.1399
              ],
              [
                62,
                3.6345
              ],
              [
                64,
                0.9256
              ]
            ]
          },
          {
            "symbol": "Cu",
            "isotopes": [
              [
                63,
                69.17
              ],
              [
                65,
                30.83
              ]
            ]
          },
          {
            "symbol": "Zn",
            "isotopes": [
              [
                64,
                48.63
              ],
              [
                66,
                27.9
              ],
              [
                67,
                4.1
              ],
              [
                68,
                18.75
              ],
              [
                70,
                0.62
              ]
            ]
          },
          {
            "symbol": "Ga",
            "isotopes": [
              [
                69,
                60.108
              ],
              [
                71,
                39.892
              ]
            ]
          },
          {
            "symbol": "Ge",
            "isotopes": [
              [
                70,
                20.84
              ],
              [
                72,
                27.54
              ],
              [
                73,
                7.73
              ],
              [
                74,
                36.28
              ],
              [
                76,
                7.61
              ]
            ]
          },
          {
            "symbol": "As",
            "isotopes": [
              [
                75,
                100.0
              ]
            ]
          },
          {
            "symbol": "Se",
            "isotopes": [
              [
                74,
                0.89
              ],
              [
                76,
                9.37
              ],
              [
                77,
                7.63
              ],
              [
                78,
                23.77
              ],
              [
                80,
                49.61
              ],
              [
                82,
                8.73
              ]
            ]
          },
          {
            "symbol": "Br",
            "isotopes": [
              [
                79,
                50.69
              ],
              [
                81,
                49.31
              ]
            ]
          },
          {
            "symbol": "Kr",
            "isotopes": [
              [
                78,
                0.35
              ],
              [
                80,
                2.28
              ],
              [
                82,
                11.58
              ],
              [
                83,
                11.49
              ],
              [
                84,
                57.0
              ],
              [
                86,
                17.3
              ]
            ]
          },
          {
            "symbol": "Rb",
            "isotopes": [
              [
                85,
                72.17
              ],
              [
                87,
                27.83
              ]
            ]
          },
          {
            "symbol": "Sr",
            "isotopes": [
              [
                84,
                0.56
              ],
              [
                86,
                9.86
              ],
              [
                87,
                7.0
              ],
              [
                88,
                82.58
              ]
            ]
          },
          {
            "symbol": "Y",
            "isotopes": [
              [
                89,
                100.0
              ]
            ]
          },
          {
            "symbol": "Zr",
            "isotopes": [
              [
                90,
                51.45
              ],
              [
                91,
                11.22
              ],
              [
                92,
                17.15
              ],
              [
                94,
                17.38
              ],
              [
                96,
                2.8
              ]
            ]
          },
          {
            "symbol": "Nb",
            "isotopes": [
              [
                93,
                100.0
              ]
            ]
          },
          {
            "symbol": "Mo",
            "isotopes": [
              [
                92,
                14.84
              ],
              [
                94,
                9.25
              ],
              [
                95,
                15.92
              ],
              [
                96,
                16.68
              ],
              [
                97,
                9.55
              ],
              [
                98,
                24.13
              ],
              [
                100,
                9.63
              ]
            ]
          },
          {
            "symbol": "Tc",
            "isotopes": [
              [
                98,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ru",
            "isotopes": [
              [
                96,
                5.54
              ],
              [
                98,
                1.87
              ],
              [
                99,
                12.76
              ],
              [
                100,
                12.6
              ],
              [
                101,
                17.06
              ],
              [
                102,
                31.55
              ],
              [
                104,
                18.62
              ]
            ]
          },
          {
            "symbol": "Rh",
            "isotopes": [
              [
                103,
                100.0
              ]
            ]
          },
          {
            "symbol": "Pd",
            "isotopes": [
              [
                102,
                1.02
              ],
              [
                104,
                11.14
              ],
              [
                105,
                22.33
              ],
              [
                106,
                27.33
              ],
              [
                108,
                26.46
              ],
              [
                110,
                11.72
              ]
            ]
          },
          {
            "symbol": "Ag",
            "isotopes": [
              [
                107,
                51.839
              ],
              [
                109,
                48.161
              ]
            ]
          },
          {
            "symbol": "Cd",
            "isotopes": [
              [
                106,
                1.25
              ],
              [
                108,
                0.89
              ],
              [
                110,
                12.49
              ],
              [
                111,
                12.8
              ],
              [
                112,
                24.13
              ],
              [
                113,
                12.22
              ],
              [
                114,
                28.73
              ],
              [
                116,
                7.49
              ]
            ]
          },
          {
            "symbol": "In",
            "isotopes": [
              [
                113,
                4.29
              ],
              [
                115,
                95.71
              ]
            ]
          },
          {
            "symbol": "Sn",
            "isotopes": [
              [
                112,
                0.97
              ],
              [
                114,
                0.66
              ],
              [
                115,
                0.34
              ],
              [
                116,
                14.54
              ],
              [
                117,
                7.68
              ],
              [
                118,
                24.22
              ],
              [
                119,
                8.59
              ],
              [
                120,
                32.58
              ],
              [
                122,
                4.63
              ],
              [
                124,
                5.79
              ]
            ]
          },
          {
            "symbol": "Sb",
            "isotopes": [
              [
                121,
                57.21
              ],
              [
                123,
                42.79
              ]
            ]
          },
          {
            "symbol": "Te",
            "isotopes": [
              [
                120,
                0.09
              ],
              [
                122,
                2.55
              ],
              [
                123,
                0.89
              ],
              [
                124,
                4.74
              ],
              [
                125,
                7.07
              ],
              [
                126,
                18.84
              ],
              [
                128,
                31.74
              ],
              [
                130,
                34.08
              ]
            ]
          },
          {
            "symbol": "I",
            "isotopes": [
              [
                127,
                100.0
              ]
            ]
          },
          {
            "symbol": "Xe",
            "isotopes": [
              [
                124,
                0.09
              ],
              [
                126,
                0.09
              ],
              [
                128,
                1.92
              ],
              [
                129,
                26.44
              ],
              [
                130,
                4.08
              ],
              [
                131,
                21.18
              ],
              [
                132,
                26.89
              ],
              [
                134,
                10.44
              ],
              [
                136,
                8.87
              ]
            ]
          },
          {
            "symbol": "Cs",
            "isotopes": [
              [
                133,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ba",
            "isotopes": [
              [
                130,
                0.106
              ],
              [
                132,
                0.101
              ],
              [
                134,
                2.417
              ],
              [
                135,
                6.592
              ],
              [
                136,
                7.854
              ],
              [
                137,
                11.232
              ],
              [
                138,
                71.698
              ]
            ]
          },
          {
            "symbol": "La",
            "isotopes": [
              [
                138,
                0.09
              ],
              [
                139,
                99.91
              ]
            ]
          },
          {
            "symbol": "Ce",
            "isotopes": [
              [
                136,
                0.185
              ],
              [
                138,
                0.251
              ],
              [
                140,
                88.45
              ],
              [
                142,
                11.114
              ]
            ]
          },
          {
            "symbol": "Pr",
            "isotopes": [
              [
                141,
                100.0
              ]
            ]
          },
          {
            "symbol": "Nd",
            "isotopes": [
              [
                142,
                27.2
              ],
              [
                143,
                12.2
              ],
              [
                144,
                23.8
              ],
              [
                145,
                8.3
              ],
              [
                146,
                17.2
              ],
              [
                148,
                5.7
              ],
              [
                150,
                5.6
              ]
            ]
          },
          {
            "symbol": "Pm",
            "isotopes": [
              [
                145,
                100.0
              ]
            ]
          },
          {
            "symbol": "Sm",
            "isotopes": [
              [
                144,
                3.07
              ],
              [
                147,
                14.99
              ],
              [
                148,
                11.24
              ],
              [
                149,
                13.82
              ],
              [
                150,
                7.38
              ],
              [
                152,
                46.75
              ],
              [
                154,
                22.75
              ]
            ]
          },
          {
            "symbol": "Eu",
            "isotopes": [
              [
                151,
                47.81
              ],
              [
                153,
                52.19
              ]
            ]
          },
          {
            "symbol": "Gd",
            "isotopes": [
              [
                152,
                0.2
              ],
              [
                154,
                2.18
              ],
              [
                155,
                14.8
              ],
              [
                156,
                20.47
              ],
              [
                157,
                15.65
              ],
              [
                158,
                24.84
              ],
              [
                160,
                21.86
              ]
            ]
          },
          {
            "symbol": "Tb",
            "isotopes": [
              [
                159,
                100.0
              ]
            ]
          },
          {
            "symbol": "Dy",
            "isotopes": [
              [
                156,
                0.06
              ],
              [
                158,
                0.1
              ],
              [
                160,
                2.34
              ],
              [
                161,
                18.91
              ],
              [
                162,
                25.51
              ],
              [
                163,
                24.9
              ],
              [
                164,
                28.18
              ]
            ]
          },
          {
            "symbol": "Ho",
            "isotopes": [
              [
                165,
                100.0
              ]
            ]
          },
          {
            "symbol": "Er",
            "isotopes": [
              [
                162,
                0.14
              ],
              [
                164,
                1.61
              ],
              [
                166,
                33.61
              ],
              [
                167,
                22.93
              ],
              [
                168,
                26.78
              ],
              [
                170,
                14.93
              ]
            ]
          },
          {
            "symbol": "Tm",
            "isotopes": [
              [
                169,
                100.0
              ]
            ]
          },
          {
            "symbol": "Yb",
            "isotopes": [
              [
                168,
                0.13
              ],
              [
                170,
                3.04
              ],
              [
                171,
                14.28
              ],
              [
                172,
                21.83
              ],
              [
                173,
                16.13
              ],
              [
                174,
                31.83
              ],
              [
                176,
                12.76
              ]
            ]
          },
          {
            "symbol": "Lu",
            "isotopes": [
              [
                175,
                97.41
              ],
              [
                176,
                2.59
              ]
            ]
          },
          {
            "symbol": "Hf",
            "isotopes": [
              [
                174,
                0.16
              ],
              [
                176,
                5.26
              ],
              [
                177,
                18.6
              ],
              [
                178,
                27.28
              ],
              [
                179,
                13.62
              ],
              [
                180,
                35.08
              ]
            ]
          },
          {
            "symbol": "Ta",
            "isotopes": [
              [
                180,
                0.016
              ],
              [
                181,
                99.988
              ]
            ]
          },
          {
            "symbol": "W",
            "isotopes": [
              [
                180,
                0.12
              ],
              [
                182,
                26.5
              ],
              [
                183,
                14.31
              ],
              [
                184,
                30.64
              ],
              [
                186,
                28.43
              ]
            ]
          },
          {
            "symbol": "Re",
            "isotopes": [
              [
                185,
                37.4
              ],
              [
                187,
                62.6
              ]
            ]
          },
          {
            "symbol": "Os",
            "isotopes": [
              [
                184,
                0.02
              ],
              [
                186,
                1.59
              ],
              [
                187,
                1.96
              ],
              [
                188,
                13.24
              ],
              [
                189,
                16.15
              ],
              [
                190,
                26.26
              ],
              [
                192,
                40.78
              ]
            ]
          },
          {
            "symbol": "Ir",
            "isotopes": [
              [
                191,
                37.3
              ],
              [
                193,
                62.7
              ]
            ]
          },
          {
            "symbol": "Pt",
            "isotopes": [
              [
                190,
                0.014
              ],
              [
                192,
                0.782
              ],
              [
                194,
                32.967
              ],
              [
                195,
                33.832
              ],
              [
                196,
                25.242
              ],
              [
                198,
                7.163
              ]
            ]
          },
          {
            "symbol": "Au",
            "isotopes": [
              [
                197,
                100.0
              ]
            ]
          },
          {
            "symbol": "Hg",
            "isotopes": [
              [
                196,
                0.15
              ],
              [
                198,
                9.97
              ],
              [
                199,
                16.87
              ],
              [
                200,
                23.1
              ],
              [
                201,
                13.18
              ],
              [
                202,
                29.86
              ],
              [
                204,
                6.87
              ]
            ]
          },
          {
            "symbol": "Tl",
            "isotopes": [
              [
                203,
                29.524
              ],
              [
                205,
                70.476
              ]
            ]
          },
          {
            "symbol": "Pb",
            "isotopes": [
              [
                204,
                1.4
              ],
              [
                206,
                24.1
              ],
              [
                207,
                22.1
              ],
              [
                208,
                52.4
              ]
            ]
          },
          {
            "symbol": "Bi",
            "isotopes": [
              [
                209,
                100.0
              ]
            ]
          },
          {
            "symbol": "Po",
            "isotopes": [
              [
                109,
                100.0
              ]
            ]
          },
          {
            "symbol": "At",
            "isotopes": [
              [
                210,
                100.0
              ]
            ]
          },
          {
            "symbol": "Rn",
            "isotopes": [
              [
                222,
                100.0
              ]
            ]
          },
          {
            "symbol": "Fr",
            "isotopes": [
              [
                223,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ra",
            "isotopes": [
              [
                226,
                100.0
              ]
            ]
          },
          {
            "symbol": "Ac",
            "isotopes": [
              [
                227,
                100.0
              ]
            ]
          },
          {
            "symbol": "Th",
            "isotopes": [
              [
                232,
                100.0
              ]
            ]
          },
          {
            "symbol": "Pa",
            "isotopes": [
              [
                231,
                100.0
              ]
            ]
          },
          {
            "symbol": "U",
            "isotopes": [
              [
                234,
                0.0055
              ],
              [
                235,
                0.72
              ],
              [
                238,
                99.2745
              ]
            ]
          },
          {
            "symbol": "Np",
            "isotopes": [
              [
                237,
                100.0
              ]
            ]
          },
          {
            "symbol": "Pu",
            "isotopes": [
              [
                244,
                100.0
              ]
            ]
          },
          {
            "symbol": "Am",
            "isotopes": [
              [
                243,
                100.0
              ]
            ]
          },
          {
            "symbol": "Cm",
            "isotopes": [
              [
                247,
                100.0
              ]
            ]
          },
          {
            "symbol": "Bk",
            "isotopes": [
              [
                247,
                100.0
              ]
            ]
          },
          {
            "symbol": "Cf",
            "isotopes": [
              [
                251,
                100.0
              ]
            ]
          },
          {
            "symbol": "Es",
            "isotopes": [
              [
                252,
                100.0
              ]
            ]
          },
          {
            "symbol": "Fm",
            "isotopes": [
              [
                257,
                100.0
              ]
            ]
          },
          {
            "symbol": "Md",
            "isotopes": [
              [
                258,
                100.0
              ]
            ]
          },
          {
            "symbol": "No",
            "isotopes": [
              [
                259,
                100.0
              ]
            ]
          },
          {
            "symbol": "Lr",
            "isotopes": [
              [
                262,
                100.0
              ]
            ]
          },
          {
            "symbol": "Rf",
            "isotopes": [
              [
                263,
                100.0
              ]
            ]
          },
          {
            "symbol": "Db",
            "isotopes": [
              [
                262,
                100.0
              ]
            ]
          },
          {
            "symbol": "Sg",
            "isotopes": [
              [
                266,
                100.0
              ]
            ]
          },
          {
            "symbol": "Bh",
            "isotopes": [
              [
                264,
                100.0
              ]
            ]
          },
          {
            "symbol": "Hs",
            "isotopes": [
              [
                269,
                100.0
              ]
            ]
          }
        ]
