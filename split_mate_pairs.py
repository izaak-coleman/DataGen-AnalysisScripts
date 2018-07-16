import sys


def split_mate_pairs(mixed_fname):
  left_pair  = mixed_fname[:-6] + "_1" + ".fastq"
  right_pair = mixed_fname[:-6] + "_2" + ".fastq"

  f = open(mixed_fname)
  lines = f.readlines()

  lf = open(left_pair, 'w')
  rf = open(right_pair, 'w')

  for i in xrange(0, len(lines), 8):    # print left mates
    if i >= len(lines) - 4:             # bound check 
      break

    for j in range(0,4):
      lf.write(lines[i+j])

  for i in xrange(4, len(lines), 8):    # print right mates
    if i > len(lines) - 4:             #bound check
      break

    for j in range(0,4):
      rf.write(lines[i+j])

def main():
  if (len(sys.argv) != 2):
    print "usage: <exe> <mixed_fastq>"
    print "output: mixed_fastq_1 mixed_fastq_2"
  else:
    split_mate_pairs(sys.argv[1])

main()
