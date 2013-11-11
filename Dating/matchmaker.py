import random
import operator
from itertools import combinations_with_replacement, ifilter, permutations, islice

def playRandom(candidates, numberOfAttributes):
  nextCandidate = [random.randint(0,1) for r in range(0, numberOfAttributes)]
  return nextCandidate

def playBruteForce(candidates, numberOfAttributes):
  possibleCombinationOfWeights = list(getIfilter(numberOfAttributes))
  possibleWeights = [list(permutations(weight)) for weight in possibleCombinationOfWeights]
  possibleWeights = [weight for weights in possibleWeights for weight in weights]

  (bestWeightEstimates, cumulativeDifference) = getBestWeightEstimatesAndCumulativeDifference(candidates, possibleWeights)
  possibleCandidates = getFilteredCandidateList(candidates, bestWeightEstimates)
  nextCandidate = list(possibleCandidates[0])
  return nextCandidate

def playSimulatedAnnealing(candidates, numberOfAttributes):
  possibleCombinationOfWeights = getIfilter(numberOfAttributes)
  sliceTest = sliceIfilter(possibleCombinationOfWeights, 0, 4)
  raw_input(sliceTest)

def sliceIfilter(ifilterObject, startIndex, endIndex):
  slicedIfilterObject = list(islice(ifilterObject, startIndex, endIndex))
  slicedList = [list(permutations(weight)) for weight in slicedIfilterObject]
  slicedList = [weight for weights in slicedList for weight in weights]
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

def getBestWeightEstimatesAndCumulativeDifference(candidates, possibleWeights):
  bestCumulativeDifference = float('Inf')
  bestWeightEstimates = []
  
  for testWeight in possibleWeights:
    testWeight = map(operator.mul, testWeight, [0.01 for r in range(len(testWeight))])
    cumulativeDifference = getCumulativeDifference(candidates, testWeight)
    if bestCumulativeDifference > cumulativeDifference:
      bestCumulativeDifference = cumulativeDifference
      bestWeightEstimates = [testWeight]

  return (bestWeightEstimates, bestCumulativeDifference)

def getCumulativeDifference(candidates, testWeight):
  difference = [abs(dotProduct(testWeight, candidate[0]) - candidate[1])
                for candidate
                in candidates]
  cumulativeDifference = sum(difference)
  return cumulativeDifference

def dotProduct(vector1, vector2):
  return sum(map(operator.mul, vector1, vector2))

def sumToPositiveAndNegativeValue(values, targetValue=100):
  positiveSublist = [value for value in values if value > 0]
  negativeSublist = [value for value in values if value < 0]
  if sum(positiveSublist) == targetValue and sum(negativeSublist) == -targetValue:
    return True
  return False

