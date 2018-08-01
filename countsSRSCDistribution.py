import sys
import callFormater
from itertools import groupby

def splitCallsByChromosome(calls):
 return [list(g) for k, g in groupby(calls, lambda x: [0])]
  
def splitIntosSRSC(calls, W):
  """Function uses seed and extend to group SNV calls into sSRSC."""
  sSRSCs = []
  i = 0
  while i < len(calls)-1:
    sSRSC = []
    extend = i+1
    sSRSC.append(calls[i]) # ith element seeds the next sSRSC 
    if abs(calls[i][1] - calls[extend][1]) <= W: # then extend sSRSC
      sSRSC.append(calls[extend])
      extend = extend + 1
      while extend < len(calls) and abs(calls[i][1] - calls[extend][1]) <= W:
        sSRSC.append(calls[extend])
        extend = extend + 1
    i = extend
    sSRSCs.append(sSRSC)
  
  # Last element is a 1-sSRSC
  if i == len(calls) - 1:
    sSRSC = []
    sSRSC.append(calls[i])
    sSRSCs.append(sSRSC)

  return sSRSCs

def countDistribution(all_calls, max_k, w):
  all_sSRSCs = []
  sSRSCs_by_k = [[] for i in range(0, max_k)]

  all_calls = [list(g) for k, g in groupby(all_calls, lambda x: [0])]

  # for each list of chromosome calls, split into sSRSC
  # and add to single list of sSRSC
  for calls in all_calls:
    all_sSRSCs = all_sSRSCs + splitIntosSRSC(calls, w)

  # group sSRSCs by k
  for sSRSC in all_sSRSCs:
    sSRSCs_by_k[len(sSRSC)-1].append(sSRSC)

  # count sSRSC distribution
  k_dist = []
  for k_sSRSCs in sSRSCs_by_k:
    k_dist.append(len(k_sSRSCs))

  return k_dist, sSRSCs_by_k

def printKDistribution(k_dist):
  for k in range(1, len(k_dist) + 1):
    print('%d\t%d' % (k, k_dist[k-1]))

def writesSRSCs(sSRSCs_by_k, base_name):
  for k in range(1, len(sSRSCs_by_k) +1):
    fname = base_name + '.' + str(k) + '.sSRSC.SNV_results'
    with open(fname, 'w') as f:
      i = 0
      k_sSRSCs = sSRSCs_by_k[k-1]
      for sSRSC in k_sSRSCs:
        for e in sSRSC:
          f.write(str(i) + '\t' + 'SNV' + '\t' + '\t'.join([str(x) for x in e]) + '\n')
          i = i + 1


def main():
  if len(sys.argv) != 4:
    print("Usage: <exe> <gedi_calls> <max_k> <W>")
    sys.exit(1)

  max_k = int(sys.argv[2])
  w = int(sys.argv[3])
  # get input file as calls list
  all_calls = callFormater.gediToCalls(sys.argv[1])
  k_dist, sSRSCs_by_k = countDistribution(all_calls, max_k, w)

  printKDistribution(k_dist)
  writesSRSCs(sSRSCs_by_k, sys.argv[1][:-12])

if __name__ == '__main__':
  main()
