import sys
import itertools
import time

def Mint1(denominations,N,minScoreSoFar):
  denominations = sorted(denominations, reverse=True)

  # Store the number of coins required to get the price.
  # Initialize price 0 to 0.
  numberOfCoins = [float('Inf'),]*100
  numberOfCoins[0] = 0

  score = 0
  for i in range(1, len(numberOfCoins)):
    # Look for all the prices that, added to value of one
    # of the denominations could give us the current price.
    possibleSubValues = [float('Inf'),]*len(denominations)
    for j in range(0, len(denominations)):
      subValue = i - denominations[j]
      if subValue >= 0:
        possibleSubValues[j] = subValue
    # Extract those subValues that are not Inf and get the
    # number of coins associated with those sub-values.
    possibleSubValues = [k for k in possibleSubValues if k != float('Inf')]
    numberOfCoins[i] = min([numberOfCoins[k] for k in possibleSubValues]) + 1

    # Update the score. For multiples of 5 modify by N.
    if i % 5 == 0:
      score = score + (N * numberOfCoins[i])
    else:
      score = score + numberOfCoins[i]

    # If the score is greater than the inputed
    # minScoreSoFar, exit with value Inf.
    if score > minScoreSoFar:
      score = float('Inf')
      return score

  return score

def GetDenominations(N, problemNumber):
  print("Temp")

  # Inform best score on previous knowledge
  bestScore = float('Inf')
  if problemNumber == 1:
    bestDenomination = [33, 23, 16, 5, 1]
    bestScore = Mint1(bestDenomination, N, bestScore)
  else:
    raise Exception("problemNumber must be 1 or 2 only")

  # Determine best score.
  permutations = tuple(itertools.combinations(tuple(range(2, 51)), 4));
  for i in range(0, len(permutations)):
    denomination = sorted(permutations[i] + (1,), reverse=True)
    if problemNumber == 1:
      score = Mint1(denomination, N, bestScore)
    else:
      raise Exception("problemNumber must be 1 or 2 only")

    if score < bestScore:
      bestScore = score
      bestDenomination = denomination
  print(bestDenomination)

if __name__ == '__main__':
  startTime = time.time()
  N = float(sys.argv[1])
  problemNumber = int(sys.argv[2])

  GetDenominations(N, problemNumber)

  endTime = time.time()
  print("Elapsed time: %g seconds" % (endTime - startTime))
