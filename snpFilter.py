import sys

def snpFilter(snp_fname, calls_fname):
  snps = []
  calls = []
  with open(snp_fname) as f:
    snps = [l.strip().split('\t') for l in f]
    snps = [(e[0],e[1], e[7].split('/')) for e in snps]
  with open(calls_fname) as f:
    calls = [l.strip().split('\t') for l in f]
  snp_filtered_calls = []
  snp_removed = []
  for call in calls:
    if not snp(call, snps):
      snp_filtered_calls.append('\t'.join(call))
    else:
      snp_removed.append('\t'.join(call))
  with open(calls_fname+'.snp_fil','w') as f:
    f.write('\n'.join(snp_filtered_calls))
  with open(calls_fname+'.snp_rem','w') as f:
    f.write('\n'.join(snp_removed))

def snp(call, snps):
  for snp in snps:
    if (snp[0] in call) and (snp[1] in call):
      count = 0
      for variant in snp[2]:
        if variant.upper() in call:
          count = count + 1
      if count == 2:
        return True
    # else continue
  return False


def main():
  if len(sys.argv) != 3:
    print("Usage: <exe> <snp_file> <calls_file>")
    sys.exit(1)
  snpFilter(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
  main()
