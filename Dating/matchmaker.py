import operator
from random import randint
from itertools import combinations_with_replacement, ifilter, permutations, islice

def playRandom(candidates, numberOfAttributes):
  nextCandidate = [randint(0,1) for r in range(0, numberOfAttributes)]
  return nextCandidate

def playBruteForce(candidates, numberOfAttributes):
  possibleCombinationOfWeights = list(getIfilter(numberOfAttributes))
  possibleWeights = getPermutationOfWeights(possibleCombinationOfWeights)

  (bestWeights, _) = getBestWeights(candidates, possibleWeights)
  possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
  nextCandidate = list(possibleCandidates[0])
  return nextCandidate

def playSimulatedAnnealing(candidates, numberOfAttributes):
  cumulativeDifferences = (float('Inf'), float('Inf'), -float('Inf'))
  bestWeights = []

  while True:
    randomWeightSelection = [getRandomWeightSelection(numberOfAttributes) for _ in range(10000)]
    #weightSelection = list(set(getPermutationOfWeights(randomWeightSelection)))
    (thisBestWeights, thisCumulativeDifference) = getBestWeights(candidates, randomWeightSelection)
    if (cumulativeDifferences[0] > thisCumulativeDifference[0]
        and cumulativeDifferences[1] > thisCumulativeDifference[1]
        and cumulativeDifferences[2] < thisCumulativeDifference[2]):
      bestWeights = thisBestWeights
      cumulativeDifferences = thisCumulativeDifference
      print(cumulativeDifferences)
    if cumulativeDifferences[1] < 0.2 and cumulativeDifferences[2] < 0.1:
      break

  possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
  nextCandidate = list(possibleCandidates[0])
  return nextCandidate

def getRandomWeightSelection(numberOfAttributes):
  numberOfNegativeWeights = randint(1, numberOfAttributes-1)
  numberOfPositiveWeights = numberOfAttributes-numberOfNegativeWeights

  negativeWeights = getRandomWeightSelection_(numberOfNegativeWeights, numberOfAttributes, True)
  positiveWeights = getRandomWeightSelection_(numberOfPositiveWeights, numberOfAttributes, False)
  weights = tuple(positiveWeights+negativeWeights)
  return weights

def getRandomWeightSelection_(numberOfWeights, numberOfAttributes, isNegative):
  weights = []
  for i in range(numberOfWeights):
    currentSum = sum(weights)
    maxAdd = (100-currentSum)
    if i == numberOfWeights-1:
      weight = maxAdd
    else:
      weight = randint(0, maxAdd)
    weights += [weight]

  if isNegative:
    weights = map(operator.mul, weights, [-1 for r in range(len(weights))])
  return weights

def getPermutationOfWeights(unpermutedList):
  permutedListOfList = [list(permutations(x)) for x in unpermutedList]
  permutedList = [x for permutedList in permutedListOfList for x in permutedList]
  return permutedList


def sliceIfilter(ifilterObject, startIndex, endIndex):
  slicedIfilterObject = list(islice(ifilterObject, startIndex, endIndex))
  slicedList = getPermutationOfWeights(slicedIfilterObject)
  return slicedList

def getIfilter(numberOfAttributes):
  return ifilter(sumToPositiveAndNegativeValue,
                 combinations_with_replacement(range(-100, 101),
                 numberOfAttributes)
                )

def getFilteredCandidateList(candidates, weightEstimates):
  candidatesList = [tuple(candidate[0]) for candidate in candidates]
  possibleCandidates = list(
                            set(
                                [tuple([1 if value > 0 else 0 for value in weightEstimate])
                                 for weightEstimate in weightEstimates]
                               )
                           )
  filteredPossibleCandidates = [possibleCandidate for possibleCandidate in possibleCandidates if possibleCandidate not in candidatesList]
  return filteredPossibleCandidates

def getBestWeights(candidates, possibleWeights):
  bestCumulativeDifference = tuple([float('Inf') for r in range(3)])
  bestWeightEstimates = []
  
  for testWeight in possibleWeights:
    testWeight = map(operator.mul, testWeight, [0.01 for r in range(len(testWeight))])
    cumulativeDifference = getCumulativeDifference(candidates, testWeight)
    if bestCumulativeDifference[0] > cumulativeDifference[0]:
      bestCumulativeDifference = cumulativeDifference
      bestWeightEstimates = [testWeight]

  return (bestWeightEstimates, bestCumulativeDifference)

def getCumulativeDifference(candidates, testWeight):
  difference = [dotProduct(testWeight, candidate[0]) - candidate[1]
                for candidate
                in candidates]
  cumulativeDifference = sum(map(abs, difference))
  positiveCumulativeDifference = sum([x for x in difference if x > 0])
  negativeCumulativeDifference = sum([x for x in difference if x < 0])
  return (cumulativeDifference, positiveCumulativeDifference, negativeCumulativeDifference)

def dotProduct(vector1, vector2):
  return sum(map(operator.mul, vector1, vector2))

def sumToPositiveAndNegativeValue(values, targetValue=100):
  positiveSublist = [value for value in values if value > 0]
  negativeSublist = [value for value in values if value < 0]
  if sum(positiveSublist) == targetValue and sum(negativeSublist) == -targetValue:
    return True
  return False

