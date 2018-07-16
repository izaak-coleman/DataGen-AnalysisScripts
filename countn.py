import sys
def add_snvs(fa_name):
    fa_string = ""
    f = open(fa_name)
    lines = f.readlines()

    header =  lines.pop(0) # remove header
    for line in lines:
        fa_string += line.rstrip()
  
    #convert fa_strin to muatable list
    fa_string = list(fa_string)
    aftern(fa_string)


def aftern(dna):
  n = 1
  for char in dna:
    if char == "N":
      n = n + 1
    else:
      print n-1
      return n-1


def main():
  add_snvs(sys.argv[1]);

main()
