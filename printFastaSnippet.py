import sys
import random
from subprocess import check_output

def getValidSnippet(fa, sz, chromosome):
  """Selects a random substring of fa of length sz. Centromere sequence
     is absent from the substring. Returns, base-1 position of substring, 
     base-1 position of substring end and the substring. """
  random.seed()
  while True:
    pos = random.randint(0, len(fa))
    with open('/data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/target.bed', 'w') as f:
      f.write(chromosome + '\t%d\t%d\n' % (pos + 1, pos + sz))
    bedRes = check_output(['/data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/bedtools2/bin/bedtools intersect -v -a /data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/target.bed -b /data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/centromeres.bed'],shell=True)
    if bedRes != '':
      return (pos + 1), (pos + sz), fa[pos:pos+sz]
    else:
      print("Failed target %d - %d" % ((pos + 1), (pos + sz)))

def printFastaSnippetRand(fname, outfname, sz, chromosome):
  fasta = []
  hdr = ""
  with open(fname) as f:
    fasta = [l.strip() for l in f]
    hdr = fasta.pop(0)
    fasta = ''.join(fasta)
  snippet_start, snippet_end, snippet = getValidSnippet(fasta, sz, chromosome)
  snippet = '\n'.join([snippet[i:i+80] for i in range(0, len(snippet), 80)])
  with open(outfname, 'w') as f:
    f.write(hdr + ':' + str(snippet_start) + '-' + str(snippet_end) + '\n' + snippet)

def printFastaSnippet(fname, outfname, sz, snippet_start):
  fasta = []
  hdr = ""
  with open(fname) as f:
    fasta = [l.strip() for l in f]
    hdr = fasta.pop(0)
    fasta = ''.join(fasta)
  snippet = fasta[snippet_start-1:snippet_start-1+sz]
  snippet_end = snippet_start-1+sz
  snippet = '\n'.join([snippet[i:i+80] for i in range(0, len(snippet), 80)])
  with open(outfname, 'w') as f:
    f.write(hdr + ':' + str(snippet_start) + '-' + str(snippet_end) + '\n' + snippet)


def main():
  if len(sys.argv) != 5:
    print('Usage: <exe> <fasta> <snippet_sz> <chromosome/pos> <output_name>')
    sys.exit(1)
  if len(sys.argv) == 5:
#    printFastaSnippetRand(sys.argv[1], sys.argv[4], int(sys.argv[2]), sys.argv[3])
    printFastaSnippet(sys.argv[1], sys.argv[4], int(sys.argv[2]), int(sys.argv[3]))

if '__main__' == __name__:
  main()
