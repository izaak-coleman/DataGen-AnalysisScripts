import sys
import callFormater
W = 100

def splitIntosSRSC(calls):
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

def loadsSRSCLists(base_name, k_max):
  """Splits the real sSRSC present in the dataset by K, reading in from mlist
  files"""
  k_max = int(k_max)
  all_sSRSCs = []
  for k in range(1, int(k_max)+1):
    fname = base_name + 'm.' + str(k) + '.mlist'
    snvs = callFormater.mlistToCalls(fname)
    snvs = sorted(snvs, key=lambda x : x[1])
    all_sSRSCs.append(splitIntosSRSC(snvs))

  for k in range(1, int(k_max)+1):
    fname = base_name + 'p.' + str(k) + '.mlist'
    snvs = callFormater.mlistToCalls(fname)
    snvs = sorted(snvs, key=lambda x : x[1])
    all_sSRSCs[k-1] = all_sSRSCs[k-1] + splitIntosSRSC(snvs)
  return all_sSRSCs

def countFalsePositivesByK(real_sSRSC, called_sSRSC):
  k_false_positives = [0 for i in range(0, len(real_sSRSC))]
  for k in range(0, len(real_sSRSC)):
    for c in real_sSRSC[k]:
      print '\n'
      print called_sSRSC
      print c
      index = findClusterIndex(c, called_sSRSC)
      print index
      if index == -1:
        continue # caller did not find any SNVs in c
      e = called_sSRSC.pop(index)
      print "N FP in clust: ", numberOfFPsInCluster(e,c)
      k_false_positives[k] = k_false_positives[k] + numberOfFPsInCluster(e,c)
    remaining_k_sSRSC = [e for e in called_sSRSC if len(e) == (k+1)]
    print "remaining k sSRSC", (k+1), remaining_k_sSRSC
    for e in remaining_k_sSRSC:
      k_false_positives[k] = k_false_positives[k] + len(e)
  return k_false_positives

def findClusterIndex(c, called_sSRSC):
  for i in range(0, len(called_sSRSC)):
    for snv in c:
      if snv in called_sSRSC[i]:
        return i
  return -1

def numberOfFPsInCluster(e,c):
  counter = 0
  for snv in c:
    if snv in e:
      counter = counter + 1
  return len(e) - counter


def main():
  if len(sys.argv) != 4:
    print("Usage <exe> <mlist_base_name> <k> <gedi_calls>")
    sys.exit(1)
  real_sSRSC = loadsSRSCLists(sys.argv[1], sys.argv[2]) # mlist base, k
  gedi_sSRSC = splitIntosSRSC(callFormater.gediToCalls(sys.argv[3]))
  for e in gedi_sSRSC:
    print e
  false_positives_by_k = countFalsePositivesByK(real_sSRSC, gedi_sSRSC)
  for e in false_positives_by_k:
    print e

if __name__ == '__main__':
  main()
