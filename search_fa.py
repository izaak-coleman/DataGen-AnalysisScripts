# -*- coding: utf-8 -*-
import sys
def search():
  if len(sys.argv) != 3:
    print "Usage: <exe> <.fa> <string>"
    sys.exit(1)

  # read file
  fa = []
  with open(sys.argv[1]) as f:
    fa = [l.strip() for l in f]

  fa.pop(0) # remove header line
  fa = "".join(fa) # stringfy list

  idx = fa.find(sys.argv[2])  # find pattern
  if idx == -1:
    print "%s not present in forward" % (sys.argv[2])
  else:
    print "%s at location %d in forward complement" % (sys.argv[2], idx+1)

  # get reverse complement
  rc = "".join([{'A':'T', 'T':'A', 'C':'G', 'G':'C'}[ch] for ch in sys.argv[2]][::-1])

  idx = fa.find(rc) # find pattern
  if idx == -1:
    print "%s not present in reverse" % (sys.argv[2])
  else:
    print "%s at location %d in reverse complement" % (rc, idx+1)

def startEndOfNonN():
  if len(sys.argv) != 2:
    print "Usage: <exe> <.fa>"
    sys.exit(1)

  # read file
  fa = []
  with open(sys.argv[1]) as f:
    fa = [l.strip() for l in f]

  fa.pop(0) # remove header line
  fa = "".join(fa) # stringfy list

  end = 0
  while fa[end] == 'N':
    end = end + 1

  start = end

  while fa[start] != 'N':
    start = start + 1
  print "end of N: %d, start of N: %d" % (end, start)
  print ".fa size: %d" % (len(fa))

def countLoneN():
  """Counts the total number of 'N' characters, flanked by
    non 'N' characters"""

  if len(sys.argv) != 2:
    print "Usage: <exe> <.fa>"
    print countLoneN.__doc__
    sys.exit(1)
  fa = []
  with open(sys.argv[1]) as f:
    fa = [line.strip() for line in f]
  fa.pop(0) 
  fa = "".join(fa)

  count = 0
  for i in range(1, len(fa)):
    if i == len(fa) -1:
      continue
    if fa[i-1] != 'N' and fa[i] == 'N' and fa[i+1] != 'N':
      count = count + 1
  print count

def charConsensus():
  """ charConsensus() reads in a fasta file and prints the consesnus
    count of each encountered character in the fasta sequence in the fasta
    file"""

  if len(sys.argv) != 2:
    print "Usage: <exe> <.fa>"
    print charConsensus.__doc__
    sys.exit(1)

  fa = []
  with open(sys.argv[1]) as f:
    fa = [line.strip() for line in f]
  fa.pop(0)
  fa = "".join(fa)

  consensus = {}
  for ch in fa:
    if ch in consensus.keys():
      consensus[ch] = consensus[ch] + 1
    else:
      consensus[ch] = 1

  print "Consensus results:"
  for k, v in consensus.items():
    print "%s -- %d" % (k, v)


def main():
  search()

if __name__ == "__main__":
  main()













