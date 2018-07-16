# ShrageSim adds indels and SNPs.
# Accordingly, we need to filter vcf file to consider just SNPs.
# Strangely (and incorrectly) ShRangeSim too considers lowercase
# characters different to upper case. Consequently, many of the variant
# SNPs have caused no change in base e.g  variant is
# a -> A.  These must be filtered out

import sys

def countDistribution(fname, max_k, w):
  var_pos = []
  w = int(w)
  max_k = int(max_k)

  k_histogram = [0 for i in range(0, max_k+1)]
  mutations = [[] for i in range(0, max_k+1)]

  # extract positions from vcf as ints
  with open(fname) as f:
    var_pos = [l.strip().split('\t') for l in f]
    if var_pos[0] == 'POS':
      var_pos.pop(0)
    # Select only SNPs
    var_pos = [e for e in var_pos if e[2][-3:] == 'SNP']
    # Remove same base SNPs
    var_pos = [e for e in var_pos if e[3].upper() != e[4].upper()]
    var_pos = [[e[0], int(e[1]), e[2], e[3].upper(), e[4].upper()] + e[5:] for e in var_pos]
  i = 0

  while i < len(var_pos)-1:
    SRSC = []
    k = 1
    seed = i
    SRSC.append(var_pos[i])
    if abs(var_pos[i][1] - var_pos[seed+1][1]) <= w:
      k = k + 1
      seed = seed + 1
      SRSC.append(var_pos[seed])
      while seed  < len(var_pos)-1 and abs(var_pos[i][1] - var_pos[seed+1][1]) <= w:
        seed = seed + 1
        SRSC.append(var_pos[seed])
        k = k + 1
      i = seed + 1
    else:
      i = i + 1
    if k <= max_k:
      k_histogram[k] = k_histogram[k] + 1
      mutations[k].append(SRSC)
  return k_histogram, mutations

def printKHistogram(k_histogram):
  for k in range(0, len(k_histogram)):
    print("%d: %d" % (k, k_histogram[k]))
def string_list(l):
    return [str(e) for e in l]
def printMutations(mut, base_name):
  for k in range(0, len(mut)):
    with open(base_name + '.' + str(k) + '.vcf','w') as f:
      for SRSC in mut[k]:
        f.write('\n'.join(['\t'.join(string_list(e)) for e in SRSC]) + '\n')

def main():
  if len(sys.argv) != 4:
    print("Usage: <exe> <vcf> <max_k> <w>")
    sys.exit(1)
  k_hist , mut= countDistribution(sys.argv[1], sys.argv[2], sys.argv[3])
  base_name = sys.argv[1][:-4]
  printKHistogram(k_hist)
  printMutations(mut, base_name)

if '__main__' == __name__:
  main()
