import sys
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
  k_max = int(k_max)
  all_sSRSCs = []
  for k in range(1, int(k_max)+1):
    fname = base_name + 'm.' + str(k) + '.mlist'
    with open(fname) as f:
      snvs = [l.strip().split('\t') for l in f]
      snvs = [(e[0], int(e[1]), e[2], e[3]) for e in snvs]
    snvs = sorted(snvs, key=lambda x : x[1])
    all_sSRSCs.append(splitIntosSRSC(snvs))

  for k in range(1, int(k_max)+1):
    fname = base_name + 'p.' + str(k) + '.mlist'
    with open(fname) as f:
      snvs = [l.strip().split('\t') for l in f]
      snvs = [(e[0], int(e[1]), e[2], e[3]) for e in snvs]
    snvs = sorted(snvs, key=lambda x : x[1])
    all_sSRSCs[k-1] = all_sSRSCs[k] + splitIntosSRSC(snvs)
