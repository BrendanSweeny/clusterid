'''Functions associated with the Find Matches behavior of ClusterID'''

# Finds all possible ways to partition the target value
# with the values contained in a list.
# Recursively finds each combination by incrementing last value in list by +1 until no remainder,
# then increments the second to last by +1, etc.

# Returns a set of sets (each being a suitable combination)
def recursiveFindCombinations(target, numList, tol, depth=0, combination=[], answer=set()):
  if numList != []:
    maxIons = int(target // numList[0]) + 1

    # Adds an additional multiple of the current value for each iteration
    for i in range(0, maxIons + 1):

      # Most target values will be integers. This allows for some tolerance between precise atomic
      # masses and imprecise target value
      # if math.isclose(target, numList[0] * i, abs_tol=1):
      if abs(target - numList[0] * i) <= tol:
        remainder = 0
      else:
        remainder = target - (numList[0] * i)
      combination[depth] = i

      # Terminating case: when the target is matched, combo list is copied
      if numList[1:] == [] and remainder == 0:
        answer.add(tuple(combination[:]))
      #print('n:', numList[0], 'maxIons:', maxIons, 'i:', i, 'total:', i * numList[0], 'remainder:', remainder, 'numList:', numList[1:], 'combo:', combination, 'answer:', answer)

      # Recursion: calls the function for the next value in numList
      recursiveFindCombinations(remainder, numList[1:], tol, depth + 1, combination, answer)
  return answer

# Finds the precise mass of the match, used to calculate % difference
# Takes a set or list as combination and list of selected elements
# Returns a float
def findPreciseMassFromCombination(combination, includeList):
  total = 0
  for i in range(len(combination)):
    total = total + combination[i] * includeList[i]
  return total

# Finds total number of unique elements in a match, used to sort returned matches
def findNumberOfElements(combination):
    totalUniqueElements = 0
    for i in combination:
        if i:
            totalUniqueElements += 1
    return totalUniqueElements
