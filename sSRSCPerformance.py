import sys
import callFormater
import countsSRSCHits as h
import countsSRSCFalsePositives as fp

def parseDatasets(fname):
  """A file is passed in containing basename - caller output filename pairs. 
     These are parsed, generating tuples of (basename, caller) strings"""
  pairs = []
  with open(fname) as f:
    pairs = [tuple(l.strip().split(',')) for l in f]
  return pairs

def calculateSensitivity(pairs, k_max):
  all_dataset_snv_total = [0 for i in range(0,k_max)]
  all_dataset_caller_hit  = [0 for i in range(0,k_max)]
  for base_name, call_file in pairs:
    total_snv_by_k = h.countTotalsSRSCByK(base_name, int(k_max))
    caller_sSRSC = callFormater.mutectToCalls(call_file)
    caller_hits_by_k = h.countsSRSCHitsByK(base_name, caller_sSRSC, int(k_max))
    for k in range(0, k_max):
      all_dataset_snv_total[k] = all_dataset_snv_total[k] + total_snv_by_k[k]
      all_dataset_caller_hit[k] = all_dataset_caller_hit[k] + caller_hits_by_k[k]
  sensitivity_by_k = []
  for k in range(0,k_max):
    try:
      s = (float(all_dataset_caller_hit[k]) / all_dataset_snv_total[k])
      sensitivity_by_k.append(s)
    except ZeroDivisionError:
      sensitivity_by_k.append(0)
  return sensitivity_by_k

def calculatePrecision(pairs, k_max):
  all_dataset_caller_hit = [0 for i in range(0,k_max)]
  all_dataset_false_positive = [0 for i in range(0,k_max)]
  for base_name, call_file in pairs:
    caller_sSRSC = callFormater.mutectToCalls(call_file)
    caller_hits_by_k = h.countsSRSCHitsByK(base_name, caller_sSRSC, int(k_max))
    real_sSRSC = fp.loadsSRSCLists(base_name, int(k_max))
    gedi_sSRSC = fp.splitIntosSRSC(callFormater.mutectToCalls(call_file))
    caller_fp_by_k = fp.countFalsePositivesByK(real_sSRSC, gedi_sSRSC)

    for k in range(0, k_max):
      all_dataset_caller_hit[k] = all_dataset_caller_hit[k] + caller_hits_by_k[k]
      all_dataset_false_positive[k] = all_dataset_false_positive[k] + caller_fp_by_k[k]
  precision_by_k = []
  for k in range(0,k_max):
    try:
      p = float(all_dataset_caller_hit[k]) / (all_dataset_caller_hit[k] + all_dataset_false_positive[k])
      precision_by_k.append(p)
    except ZeroDivisionError:
      precision_by_k.append(0)
  return precision_by_k

def main():
  if len(sys.argv) != 3:
    print("Usage: <exe> <basename/caller dataset pair list> <max_k>")
    sys.exit(1)
  pairs = parseDatasets(sys.argv[1])
  recall = calculateSensitivity(pairs, int(sys.argv[2]))
  prec = calculatePrecision(pairs, int(sys.argv[2]))
  print("k,recall,precision")
  for i in range(1,int(sys.argv[2])+1):
    print "%d, %.2f, %.2f" % (i, recall[i-1], prec[i-1])



if __name__ == '__main__':
  main()
