import sys
import calculatesSRSCSensitivity as calc

def main():
  if len(sys.argv) != 4:
    print("Usage: <exe> <base_vcf_name> <MuTect_calls> <k_max>")
    sys.exit(1)
  calls = []
  with open(sys.argv[2]) as f:
    calls = [l.strip().split('\t') for l in f]
    calls = [(e[0], int(e[1]), e[3], e[4]) for e in calls]
  k_sSRSC = calc.calculatesSRSCSensitivity(sys.argv[1], calls, int(sys.argv[3]))
  calc.printResults(k_sSRSC)

if __name__ == '__main__':
  main()
