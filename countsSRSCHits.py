import sys
import callFormater

def countsSRSCHitsByK(base_name, called_sSRSC, k_max):
  sSRSC_hits_by_k = [0 for i in range(0, k_max)]
  for k in range(1, int(k_max)+1):
    m_fname = base_name + 'm.' + str(k) + '.mlist'
    p_fname = base_name + 'p.' + str(k) + '.mlist'
    k_sSRSC = callFormater.mlistToCalls(m_fname)
    k_sSRSC = k_sSRSC + callFormater.mlistToCalls(p_fname)
    n_hits = 0
    for call in called_sSRSC:
      if call in k_sSRSC:
        n_hits = n_hits + 1
    sSRSC_hits_by_k[k-1] = n_hits
  return sSRSC_hits_by_k

def countTotalsSRSCByK(base_name, k_max):
  total_by_k = []
  for k in range(1, int(k_max)+1):
    m_fname = base_name + 'm.' + str(k) + '.mlist'
    p_fname = base_name + 'p.' + str(k) + '.mlist'
    k_sSRSC = callFormater.mlistToCalls(m_fname)
    k_sSRSC = k_sSRSC + callFormater.mlistToCalls(p_fname)
    total_by_k.append(len(k_sSRSC))
  return total_by_k


def main():
  if len(sys.argv) != 4:
    print("Usage <exe> <mlist_base_name> <k> <gedi_calls>")
    sys.exit(1)
  gedi_sSRSC = callFormater.gediToCalls(sys.argv[3])
  n_hits_by_k = countsSRSCHitsByK(sys.argv[1], gedi_sSRSC, int(sys.argv[2]))
  for e in n_hits_by_k:
    print e


if __name__ == '__main__':
  main()
