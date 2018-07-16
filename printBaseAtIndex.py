import sys

def printBaseAtIndex(fasta, index):
  """ Prints the character at a specified base-1 index in the
      provided fasta file."""
  return fasta[int(index)-1]

def loadFasta(fname):
  fasta = []
  with open(fname) as f:
    fasta = [line.strip() for line in f]
  fasta.pop(0)
  return "".join(fasta)

def main():
  if len(sys.argv) != 3:
    print "Usage: <exe> <.fa> <index>"
    print printBaseAtIndex.__doc__
    sys.exit(1)

  print printBaseAtIndex(loadFasta(sys.argv[1]), sys.argv[2])

if __name__ == "__main__":
  main()
