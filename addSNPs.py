import sys

def addSNPs(fasta, snp_list):
  """For each (pos, [variant_list]) tuple of snp_list changes the
     character at fasta[pos] to a character in variant_list that is
     != fasta[pos]."""
  fasta = list(fasta) # make mutable
  for pos, variant_list in snp_list:
    pos = pos - 1 # convert to 0-based index
    counter = 0
    while (counter < len(variant_list) and fasta[pos] == variant_list[counter]):
      counter = counter + 1
    if counter == len(variant_list):
      continue
    fasta[pos] = variant_list[counter]
  fasta = ''.join(fasta)
  return '\n'.join([fasta[i:i+80] for i in range(0, len(fasta), 80)])

def extractSNPList(fname):
  """Extracts the position and variants of each snp"""
  snp_list = []
  with open(fname) as f:
    snp_list = [l.strip() for l in f]
    snp_list = [(int(l.split('\t')[2]), list(l.split('\t')[7].split('/'))) for l in snp_list]
  return snp_list # return (pos, [variant_list]) tuples

def loadFastq(fname):
  """Load fastq data as a single string"""
  fq = []
  with open(fname) as f:
    fq = [l.strip() for l in f]
  hdr = fq.pop(0)
  return hdr, ''.join(fq)
  
def main():
  if len(sys.argv) != 4:
    print('Usage: <exe> <fastq> <snp_list> <out_fq>')
    sys.exit(1)
  snp_list = extractSNPList(sys.argv[2])
  hdr, fa = loadFastq(sys.argv[1])
  fa = addSNPs(fa, snp_list)
  with open(sys.argv[3], 'w') as f:
    f.write(hdr + '\n' + fa)

if '__main__' == __name__:
  main()
