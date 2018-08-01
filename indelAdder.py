import sys
import random
from subprocess import check_output


def inCentromere(chromosome, bed_path, bound):
  with open(bed_path + 'indel.bed', 'w') as f:
    f.write(chromosome + '\t%d\t%d\n' % (bound[0], bound[1]))
  cmd = (bed_path + 'bedtools intersect -v -a ' + 
         bed_path + 'indel.bed -b ' + bed_path + 'centromeres.bed')
  bed_res = check_output([cmd], shell=True)
  if bed_res == '':
    return True
  return False  

def overlappedBounds(bound, indel_bounds):
  for l,h in indel_bounds:
    if (l <= bound[0] and bound[0] < h) or (l <= bound[0] and h < bound[0]):
      return True
  return False

def getValidIndelBounds(chromosome, n_indels, fasta_len, bed_path, max_indel_sz):
  random.seed()
  indel_bounds = []
  while len(indel_bounds) != n_indels:
    indel_size = random.randint(1, int(max_indel_sz))
    bound = random.randint(0, fasta_len  - indel_size)
    bound = (bound, bound + indel_size)
    if inCentromere(chromosome, bed_path, bound): 
      continue
    if overlappedBounds(bound, indel_bounds): 
       continue
    indel_bounds.append(bound)
    return sorted(indel_bounds, key=lambda x: x[0])

def addIndel(fasta, b):
  insertion = random.choice([True, False])
  if insertion:
    length = b[1] - b[0]
    substring =  ''.join(random.choice('ATCG') for x in range(length))
    print b 
    print substring
    return fasta[:b[0] + 1] + list(substring) + fasta[b[0] + 1 :]
  else: # deletion
    return fasta[:b[0] + 1] + fasta[b[1] + 1:]

def addIndels(bounds, fasta):
  fasta = list(fasta)
  for b in bounds:
    fasta = addIndel(fasta, b)
  return ''.join(fasta)



def main():
  if len(sys.argv) != 6:
    print("usage: <exe> <chromosome> <bed_path> <n_indels> <fasta_file> <max_indel_sz>")
    sys.exit(1)
  fasta = ''
  with open(sys.argv[4]) as f:
    fasta = [l.strip() for l in f]
    hdr  = fasta.pop(0)
    fasta = ''.join(fasta)
  bounds = getValidIndelBounds(sys.argv[1], int(sys.argv[3]), len(fasta), sys.argv[2], int(sys.argv[5]))
  fasta = addIndels(bounds, fasta)
  fasta = '\n'.join([fasta[i:i+80] for i in range(0, len(fasta), 80)])
  print(hdr)
  print(fasta)

if __name__ == '__main__':
  main()
