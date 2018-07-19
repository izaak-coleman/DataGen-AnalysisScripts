import sys
import callFormater
import calculatesSRSCSensitivity as calc

def main():
  if len(sys.argv) != 4:
    print("Usage: <exe> <base_vcf_name> <MuTect_calls> <k_max>")
    sys.exit(1)
  calls = callFormater.mutectToCalls(sys.argv[2])
  k_sSRSC = calc.calculatesSRSCSensitivity(sys.argv[1], calls, int(sys.argv[3]))
  calc.printResults(k_sSRSC)

if __name__ == '__main__':
  main()
