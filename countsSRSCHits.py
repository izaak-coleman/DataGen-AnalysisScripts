import callFormater

def countsSRSCHitsByK(base_name, called_sSRSC, k_max):
  sSRSC_hits_by_k = []
  for k in range(1, int(k_max)+1):
    fname = base_name + str(k) + '.mlist'
    k_sSRSC = callFormater.mlistToCalls(fname)
    n_hits = 0
    for call in called_sSRSC:
      if call in k_sSRSC:
        n_hits = n_hits + 1
    sSRSC_hits_by_k[k-1] = n_hits
  return sSRSC_hits_by_k

