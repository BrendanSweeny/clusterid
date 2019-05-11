# TODO: Consider moving mass calculation functions to a seperate module
# TODO: Consider moving all of these functions to a utils object so elements
#   can be imported here and removed from tofviewwidget

### VALIDATION FUNCTIONS ###

# Checks if number can be typed to float
def isFloat(value):
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True

# Checks if element symbol is in self.elements list of objects
def validElement(elements, entry):
    for element in elements:
        if entry == element['symbol']:
            return True
    return False

# Validates a list generated from formulaToList
# Validation returns True if all strings in the list match element symbols
# included in the element dicts passed as the first argument and if parentheses
# are properly matched
def validateFormulaList(elements, formulaList):
    isValid = True
    if not formulaList:
        isValid = False

    depth = 0
    for entry in formulaList:
        # Skip if it's a number
        if isFloat(entry):
            continue
        # Skip if its a parens
        elif entry == '(':
            depth += 1
        elif entry == ')':
            depth -= 1
        # Check if it's an element
        else:
            for element in elements:
                if not validElement(elements, entry):
                    isValid = False
    if depth != 0:
        isValid = False

    return isValid

### FORMATTING FUNCTIONS ###

# Recursive function that breaks up molecular formula to list of elements
# and number of each element
# Used in handleFindFormulaMass
# Returns formula list, ex. ['V', 2, 'Al', 2, 'O', 4]
def formulaToList(formula, depth=0, resultList=[], workingEntry=''):
    if formula:
        # first iteration working entry is empty string
        if not workingEntry:
            workingEntry = formula[0]
        # Case: working entry is a character and next a character
        elif workingEntry.isalpha() and formula[0].isalpha():
            #print('alpha+alpha')
            if workingEntry[-1].isupper() and formula[0].islower():
                #print('upper+lower')
                workingEntry = workingEntry + formula[0]
            elif workingEntry[-1].isupper() and formula[0].isupper():
                resultList.append(workingEntry)
                resultList.append(1)
                workingEntry = formula[0]
            elif workingEntry[-1].islower() and formula[0].isupper():
                resultList.append(workingEntry)
                resultList.append(1)
                workingEntry = formula[0]
        # Case: working entry is a character or number and next is a parens
        elif workingEntry.isdigit() and (formula[0] == '(' or formula[0] == ')'):
            #print('num+paren')
            resultList.append(int(workingEntry))
            workingEntry = formula[0]
        elif workingEntry.isalpha() and (formula[0] == '(' or formula[0] == ')'):
            #print('alpha+paren')
            resultList.append(workingEntry)
            resultList.append(1)
            workingEntry = formula[0]
        # Case: where working entry is a closed paren and next is character
        elif workingEntry == ')' and not formula[0].isdigit():
            #print('paren+non-num')
            resultList.append(workingEntry)
            resultList.append(1)
            workingEntry = formula[0]
        # Case: where working entry is an open paren and next is character
        elif workingEntry == '(' and formula[0].isalpha():
            #print('paren+alpha')
            resultList.append(workingEntry)
            workingEntry = formula[0]
        # Case: where working entry and next are both is an open parens
        elif workingEntry == '(' and formula[0] == '(':
            #print('paren+paren')
            resultList.append(workingEntry)
            workingEntry = formula[0]
        # Case: where working entry is a parens and next is a number
        elif (workingEntry == '(' or workingEntry == ')') and formula[0].isdigit():
            #print('paren+num')
            resultList.append(workingEntry)
            workingEntry = formula[0]
        # Case: working entry is a character and next is a number
        elif workingEntry.isalpha() and formula[0].isdigit():
            #print('alpha+num')
            resultList.append(workingEntry)
            workingEntry = formula[0]
        # Case: working entry is number and next is number
        elif workingEntry.isdigit() and formula[0].isdigit():
            #print('num+num')
            workingEntry = workingEntry + formula[0]
        # Case: working entry is number and next is a character
        elif workingEntry.isdigit() and formula[0].isalpha():
            #print('num+alpha')
            resultList.append(int(workingEntry))
            workingEntry = formula[0]
        return formulaToList(formula[1:], depth + 1, resultList[:], workingEntry)

    # Function terminates when there are no more chars in the formula str
    else:
        # Handles what's left in the workingEntry after formula str is empty
        if workingEntry.isalpha() or workingEntry == ')':
            resultList.append(workingEntry)
            resultList.append(1)
        elif workingEntry.isdigit():
            resultList.append(int(workingEntry))
        else:
            resultList.append(workingEntry)
        #print(resultList)
        return resultList

# Removes sub tags from formula string
# Used in handleformulaEmitted slot, handleRemoveMolecule click handler
# Returns a string of charaters and ints (e.g. 'V3O4')
def stripSub(formula):
    splitFormula = formula.split('<sub>')
    intermediateFormula = ''.join(splitFormula)
    splitFormula = intermediateFormula.split('</sub>')
    finalFormula = ''.join(splitFormula)
    return finalFormula

# Checks for '</sub>', '<sub>' in list
# Used in formatFormula to avoid '<sub>', '1', '</sub>', '<sub>', '0', '</sub>'
# Instead results in: '<sub>', '1', '0', '</sub>'
# Returns a boolean (e.g. True if the entry is a </sub> and is follwed by <sub>)
def subsub(inputList, index, x):
    #print(inputList, index, x)
    if index + 1 < len(inputList) and x == '</sub>' and inputList[index + 1] == '<sub>':
        return True
    elif x == '<sub>' and inputList[index - 1] == '</sub>':
        return True
    else:
        return False

# Adds sub tags to appropriate place in formula
def formatFormula(formula):
    splitFormula = list(formula)
    formattedSplitFormula = []
    for char in splitFormula:
        try:
            float(char)
        except ValueError:
            formattedSplitFormula.append(char)
        else:
            formattedSplitFormula.append('<sub>')
            formattedSplitFormula.append(char)
            formattedSplitFormula.append('</sub>')

    # Filter out '</sub>', '<sub>'
    formattedSplitFormula = [x for index, x in enumerate(formattedSplitFormula) if not subsub(formattedSplitFormula, index, x)]
    formattedFormula = ''.join(formattedSplitFormula)
    return formattedFormula

# Adds sub tags to appropriate place in formula
def formatFormulaUnicode(formula):
    unicodeDict = {'0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083',
                    '4': '\u2084', '5': '\u2085', '6': '\u2086', '7': '\u2087',
                    '8': '\u2088', '9': '\u2089'}
    splitFormula = list(formula)
    formattedSplitFormula = []
    for char in splitFormula:
        try:
            float(char)
        except ValueError:
            formattedSplitFormula.append(char)
        else:
            unicodeChar = unicodeDict[char]
            formattedSplitFormula.append(unicodeChar)
            #formattedSplitFormula.append(char)

    # Filter out '</sub>', '<sub>'
    #formattedSplitFormula = [x for index, x in enumerate(formattedSplitFormula) if not subsub(formattedSplitFormula, index, x)]
    formattedFormula = ''.join(formattedSplitFormula)
    return formattedFormula

### MATH ###

# Takes two floats/integers and returns a float/integer
def findPercentDifference(valOne, valTwo):
    return abs((valOne - valTwo)/((valOne + valTwo)/2) * 100)

### CHEMISTRY ###

# Generates a formulaList with no parentheses that is equivalent to one
# with multiple levels of parentheses passed as argument one.
# Same general algorithm structure as recursiveFindMass
#   formulaList: can be either a string or list (of elements and
#   element quantities, returned from utils.formulaToList())
def flattenFormulaList(formulaList, outputList=[], mult=1):
    if formulaList == []:
        return outputList
    else:
        outputList = formulaListDepthZero(formulaList, mult=mult)
        nextDepthFormulas = returnNextDepth(formulaList, mult=mult)
        for depth in nextDepthFormulas:
            outputList += flattenFormulaList(depth[0], mult=depth[1])
    return outputList

# Returns a formulaList consisting of only elements in depth 0
# (outside of parentheses)
def formulaListDepthZero(formulaList, mult=1):
    if type(formulaList) is not list:
        formulaList = formulaToList(formulaList)
    depth = 0
    outputList = []
    for index, entry in enumerate(formulaList):
        if type(entry) is int or formulaList[index - 1] == ')':
            continue
        elif entry == '(':
            depth += 1
        elif entry == ')':
            depth -= 1
        elif type(entry) is str and depth == 0:
            outputList.append(entry)
            outputList.append(formulaList[index + 1] * mult)
    return outputList

# ['C', 1, 'O', 1], 3 => ['C', 1, 'O', 1, 'C', 1, 'O', 1, 'C', 1, 'O', 1]
def flattenDepthZero(formulaList, mult=1):
    outputList = []
    for i in range(0, mult):
        outputList += formulaList
    return outputList

# Calculates recursively the mass of a chemical formula and allows for
# ligands and multi-layer parentheses
#   formulaList: can be either a string or list (of elements and
#   element quantities, returned from utils.formulaToList())
def recursiveFindMass(formulaList, elementsDict, mass=0, mult=1):
    if formulaList == []:
        return mass
    else:
        mass = calcMassDepthZero(formulaList, elementsDict, mult=mult)
        nextDepthFormulas = returnNextDepth(formulaList, mult=mult)
        for depth in nextDepthFormulas:
            mass += recursiveFindMass(depth[0], elementsDict, mass=mass, mult=depth[1])
            #print('depth: ', depth, mass)
        #print(nextDepthFormulas, mass)
    return mass


# Returns the mass of all elements not in parentheses (depth > 0)
def calcMassDepthZero(formulaList, elementsDict, mult=1):
    if type(formulaList) is not list:
        formulaList = formulaToList(formulaList)
    depth = 0
    totalMass = 0
    for index, entry in enumerate(formulaList):
        if type(entry) is int or formulaList[index - 1] == ')':
            continue
        elif entry == '(':
            depth += 1
        elif entry == ')':
            depth -= 1
        elif type(entry) is str and depth == 0:
            for elem in elementsDict:
                if elem['symbol'] == entry:
                    totalMass += elem['mass'] * formulaList[index + 1]
    return totalMass * mult

# Returns a list of tuples where t[0] = formula with only depth >= 1
#   (i.e. anything inside parens, strips away elements in depth = 0),
#   t[1] = multiplication factor for the formula
# Uses mult to multiply the factor for inner parens (depth >= 1)
# E.x. AlO(H2O)2(CO)3 => [(['H', 2, 'O', 1], 2), (['C', 1, 'O', 1], 3)]
def returnNextDepth(formulaList, depth=0, mult=1):
    if type(formulaList) is not list:
        formulaList = formulaToList(formulaList)
    outputList = []
    depth = 0
    currentTuple = []
    for index, entry in enumerate(formulaList):
        if entry == ')':
            depth -= 1
            if depth == 0:
                outputList.append((currentTuple, formulaList[index + 1] * mult))
                currentTuple = []
        if depth >= 1:
            currentTuple.append(entry)
        if entry == '(':
            depth += 1
        #print(entry, depth)
    return outputList

#print(flattenDepthZero(['C', 1, 'O', 1], 3))
#print(flattenFormulaList('Al2O3(CO)2'))
#print(flattenFormulaList('((((((H(He)(Be(Li(P))))2)))2))3'))
#print(flattenFormulaList('Al2(CO)2O3'))
#print(flattenFormulaList('Al2O3'))
