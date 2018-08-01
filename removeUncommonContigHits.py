import sys
import callFormater
import operator

def removeUncommonContigHits(calls):
  filtered = []
  for e in calls:
    if '_' not in e[0]:
      filtered.append(e)

  filtered = sorted(filtered, key=operator.itemgetter(0,1))
  for e in filtered:
    i = 0
    print(str(i) + '\t' + 'SNV' + '\t' + '\t'.join([str(x) for x in e]))
    i = i + 1

def main():
  if len(sys.argv) != 2:
    print("Usage: <exe> <gediCalls>")
    sys.exit(1)
  calls = callFormater.gediToCalls(sys.argv[1])
  removeUncommonContigHits(calls)

if __name__ == '__main__':
  main()
