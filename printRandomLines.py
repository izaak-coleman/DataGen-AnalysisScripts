import sys
import random

def printRandomLines(fname, n_lines):
  random.seed()
  lines = []
  with open(fname) as f:
    lines = [l.strip() for l in f]

  # Generate list of unique random numbers of length n_lines.
  rand_nums = set()
  while len(rand_nums) != int(n_lines):
    rand_nums.add(random.randint(0, len(lines)-1))

  # Select random lines from file and print.
  out = '\n'.join([lines[e] for e in rand_nums])
  print(out)


def main():
  if len(sys.argv) != 3:
    print('Usage: <exe> <file> <nlines>')
    sys.exit(1)
  printRandomLines(sys.argv[1], sys.argv[2])

if "__main__" == __name__:
  main()
