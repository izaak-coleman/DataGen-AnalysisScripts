
def calculatesSRSCSensitivity(base_name, calls, k_max):
  k_sSRSC = []
  for i in range(0, int(k_max)+1):
    fname = base_name + str(i) + '.vcf'
    var_list = []
    with open(fname) as f:
      var_list = [e.strip().split('\t') for e in f]
      var_list = [('chr' + e[0], int(e[1]), e[3], e[4]) for e in var_list]
    n_hits = 0
    for call in calls:
      if call in var_list:
        n_hits = n_hits + 1
    try:
      k_sSRSC.append( (n_hits, len(var_list), (float(n_hits)/len(var_list))) )
    except ZeroDivisionError:
      k_sSRSC.append( (n_hits, len(var_list), (0)) )
  return k_sSRSC


def printResults(k_sSRSC):
  print('\n'.join(['k: %d, hits: %d, total: %d, sens: %.5f' % (e[0], e[1][0],e[1][1], e[1][2]) for e in zip(range(0,len(k_sSRSC)), k_sSRSC)]))
