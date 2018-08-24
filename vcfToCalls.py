import callFormater
import sys

def main():
  if len(sys.argv) != 2:
    print("Usage: <exe> <vcf>")
    print("Output: vcf -> calls to std::out")

  calls = callFormater.vcfToCalls(sys.argv[1])
  print('\n'.join([('%s\t%d\t%s\t\%s' % (e[1], e[2], e[3], e[4])) for e in calls])
