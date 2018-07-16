import sys
import randomSNVAdder

def main():
  if len(sys.argv) != 8:
    print "Usage: <exe> <fa> <nClust> <o_fa_name> <line_len> <o_m_list_name> <clustSz> <dist>"
    sys.exit(1)

  fasta, mList = randomSNVAdder.randomClusterAdder(sys.argv[1], sys.argv[2], sys.argv[6], sys.argv[7])

  f=open(sys.argv[1])
  randomSNVAdder.writeFastq(f.readlines()[0], fasta, sys.argv[3], sys.argv[4])
  f.close()
  randomSNVAdder.writeSNVs(mList, sys.argv[5])

if '__main__' == __name__:
 main()

