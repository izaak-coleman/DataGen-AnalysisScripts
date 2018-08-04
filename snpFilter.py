import sys
import callFormater
def snpFilter(snp_fname, calls_fname):
  snps = []
  calls = callFormater.gediToCalls(calls_fname)
  print("Loading raw snps")
  with open(snp_fname) as f:
    snps = [l.strip().split('\t') for l in f]
    snps = [(e[0],int(e[1]), e[7].split('/')) for e in snps]
  print ("Sorting snps")
  snps = sorted(snps, key=lambda x: x[1])


  snp_filtered_calls = []
  snp_removed = []
  for call in calls:
    index = binary_search(calls[1], snps)
    if len(index) == -1:
      snp_filtered_calls.append('\t'.join([str(e) for e in call]))
      continue
    if snp(call, snps[index]):
      snp_removed.append('\t'.join([str(e) for e in call]))

  with open(calls_fname+'.snp_fil','w') as f:
    f.write('\n'.join(snp_filtered_calls))
  with open(calls_fname+'.snp_rem','w') as f:
    f.write('\n'.join(snp_removed))

def snp(call, snp):
  if (snp[0] in call) and (int(snp[1]) in call):
  count = 0
    for variant in snp[2]:
      if variant.upper() in call:
        count = count + 1
    if count == 2:
      return True
    # else continue
  return False

def binary_search(query, snps):
  left = 0
  right = len(snps)
  while left < right:
    mid = (left + right) / 2
    if snps[mid][1] == query:
      return mid
    else if snp[mid][1] > query:
      right = mid
    else:
      left = mid + 1
  return -1 




def main():
  if len(sys.argv) != 3:
    print("Usage: <exe> <snp_file> <calls_file>")
    sys.exit(1)
  snpFilter(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
  main()
