import operator
from random import randint, shuffle, choice
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
  (bestWeights, cumulativeDifferences) = getBestWeights(candidates, [getRandomWeightSelection(numberOfAttributes)])
  (currentBestWeights, currentCumulativeDifferences) = (bestWeights, cumulativeDifferences)

  maxTemperature = 4000
  for k in range(maxTemperature):
    temperature = float(k)/maxTemperature
    if randint(0,1) > temperature:
      weightSelection = [getRandomWeightSelection(numberOfAttributes) for _ in range(10)]
    else:
      weightSelection = getNeighborWeightSelecion(bestWeights)

    #weightSelection = list(set(getPermutationOfWeights(randomWeightSelection)))
    (thisBestWeights, thisCumulativeDifferences) = getBestWeights(candidates, weightSelection)
    print(thisCumulativeDifferences)

    if cumulativeDifferences[0] > thisCumulativeDifferences[0]:
      bestWeights = thisBestWeights
      cumulativeDifferences = thisCumulativeDifferences

    if cumulativeDifferences[1] < 0.1 and cumulativeDifferences[2] > -0.1:
      possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
      if len(possibleCandidates) > 0:
        break

  possibleCandidates = getFilteredCandidateList(candidates, bestWeights)
  nextCandidate = list(possibleCandidates[0])
  return nextCandidate

def getNeighborWeightSelecion(weightSelection):
  weightSelection = weightSelection[0]
  positiveWeightsIndex = [i for (i,w) in enumerate(weightSelection) if w > 0]
  negativeWeightsIndex = [i for (i,w) in enumerate(weightSelection) if w < 0]
  if len(positiveWeightsIndex) > 1:
    (index1, index2) = getTwoValidWeights(weightSelection, positiveWeightsIndex)
  else:
    (index1, index2) = getTwoValidWeights(weightSelection, negativeWeightsIndex)
  weightSelection = list(weightSelection)
  weightSelection[index1] += 0.01
  weightSelection[index2] -= 0.01
  return [tuple(weightSelection)]

def getTwoValidWeights(weights, weightIndex):
  while True:
    weightIndex1 = choice(weightIndex)
    weightIndex2 = choice(weightIndex)
    weight1 = abs(weights[weightIndex1])
    weight2 = abs(weights[weightIndex2])
    if weight1 != 1 and weight2 != 1 and weightIndex1 != weightIndex2:
      return (weightIndex1, weightIndex2)

def getRandomWeightSelection(numberOfAttributes):
  numberOfNegativeWeights = randint(1, numberOfAttributes-1)
  numberOfPositiveWeights = numberOfAttributes-numberOfNegativeWeights

  negativeWeights = getRandomWeightSelection_(numberOfNegativeWeights, numberOfAttributes, True)
  positiveWeights = getRandomWeightSelection_(numberOfPositiveWeights, numberOfAttributes, False)
  weights = positiveWeights+negativeWeights
  shuffle(weights)
  weights = tuple(weights)
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

