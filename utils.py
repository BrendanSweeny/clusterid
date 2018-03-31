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
# included in the element dicts passed as the first argument
def validateFormulaList(elements, formulaList):
    isValid = True
    if not formulaList:
        isValid = False

    for entry in formulaList:
        # Skip if it's a number
        if isFloat(entry):
            continue
        # Check if it's an element
        else:
            for element in elements:
                if not validElement(elements, entry):
                    isValid = False
    return isValid

### FORMATTING FUNCTIONS ###

# Recursive function that breaks up molecular formula to list of elements
# and number of each element
# Used in addByFormula
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
        #resultList.add(formula[0])
        return formulaToList(formula[1:], depth + 1, resultList[:], workingEntry)

    # Function terminates when there are no more chars in the formula str
    else:
        # Handles what's left in the workingEntry after formula str is empty
        if workingEntry.isalpha():
            resultList.append(workingEntry)
            resultList.append(1)
        elif workingEntry.isdigit():
            resultList.append(int(workingEntry))
        else:
            resultList.append(workingEntry)
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

### MATH ###

# Takes two floats/integers and returns a float/integer
def findPercentDifference(valOne, valTwo):
    return abs((valOne - valTwo)/((valOne + valTwo)/2) * 100)
