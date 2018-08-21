import sys
import callFormater
def snpFilter(calls, snps):
  print("Running filter")
  for call in calls:
    index = binary_search(call, snps)
    if index != -1:
      print snps[index]

def binary_search(call, snps):
  left = 0
  right = len(snps)
  mid = -1
  hit = False
  while left < right:
    mid = (left + right) / 2
    snp = snps[mid].split('\t')
    snp_pos = int(snp[1])
    if snp_pos == call[1]:
      hit = True
      break
    elif snp_pos > call[1]:
      right = mid
    else:
      left = mid + 1

  if not hit:
    return -1

  # loop to start of hits with same position
  while int(snps[mid-1].split('\t')[1]) == call[1]:
    mid = mid - 1

  while int(snps[mid].split('\t')[1]) == call[1]:
    if snps[mid].split('\t')[0] == call[0]:
      return mid
    mid = mid + 1
  return -1

def main():
  if len(sys.argv) != 3:
    print("Usage: <exe> <snp_file> <calls_file>")
    sys.exit(1)
  print("Loading data")
  calls = callFormater.gediToCalls(sys.argv[2])
  snps = []
  with open(sys.argv[1]) as f:
    snps = [l.strip() for l in f]
  snpFilter(calls, snps)

if __name__ == "__main__":
  main()
