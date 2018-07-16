import sys
import random
from subprocess import check_output

def get_valid_ranges(chromosome, n_clusters, fa_len, bed_path):
  random.seed()
  ranges = []
  while len(ranges) != n_clusters:
    r = random.randint(0, fa_len-1)
    r = (r, r+500)

    # Check range is not within a centromere
    with open(bed_path + 'sSRSC.bed', 'w') as f:
      f.write(chromosome + '\t%d\t%d\n' % (r[0], r[1]))
    cmd = (bed_path + 'bedtools intersect -v -a ' +
           bed_path + 'sSRSC.bed -b ' + bed_path +
           'centromeres.bed')
    bed_res = check_output([cmd],shell=True)
    if bed_res == '':
      print('Range: %d, %d failed centromere' %(r[0],r[1]))
      continue

    # Check range does not overlap with prevously accepted ranges
    failed = False
    for a, b in ranges:
      if (a <= r[0] and r[0] < b) or (a <= r[1] and r[1] < b):
        failed = True
        break
    if failed:
      print('Range: %d, %d failed overlap filter' %(r[0],r[1]))
      continue

    # Passed.
    ranges.append(r)
  return ranges

def load_fasta(fname):
  data = []
  header = ''
  with open(fname) as f:
    data = [l.strip() for l in f]
    header = data.pop(0)
  return header[1:], ''.join(data)

def add_clusters(chromosome, fasta, base_name, ranges, max_k):
  fasta = list(fasta)
  sSRSC_lists = [[] for i in range(0,max_k)]
  # Add sSRSC.
  for l,h in ranges:
    k = random.randint(1,max_k)
    added_snvs = []
    for i in range(0,k):
      m = random.randint(0,100)
      # Make sure gap of at least 1bp exists between snvs in cluster
      while ((m-1) in added_snvs) or (m in added_snvs) or ((m+1) in added_snvs):
        m = random.randint(0,100)
      c,t,fasta = addSNV(l+m, fasta)
      added_snvs.append(m)
      sSRSC_lists[k-1].append(chromosome + "\t%d\t%s\t%s\n" % (l+m, c, t))

  # Write data.
  fasta = ''.join(fasta)
  fasta_file = base_name + 'sSRSC.fasta'
  with open(fasta_file,'w') as f:
    f.write('\n'.join([fasta[i:i+80] for i in range(0,len(fasta), 100)]))
  for k in range(1,max_k+1):
    mlist = base_name + str(k) + '.mlist'
    with open(mlist,'w') as f:
      f.write(''.join(sSRSC_lists[k-1]))

def addSNV(pos, fasta):
  control = fasta[pos]
  bases = 'ATCG'.replace(control,'')
  tumour = random.choice(bases)
  fasta = fasta[pos] = tumour
  return control, tumour, fasta
  


def main():
  if len(sys.argv) != 6:
    print("Usage: <exe> <p.fa> <m.fa> <n_clusters> <bed_path> <max_k>")
    sys.exit(1)
  chromosome, p_fasta = load_fasta(sys.argv[1])
  m_fasta = load_fasta(sys.argv[2])
  ranges = get_valid_ranges(chromosome, int(sys.argv[3]), len(p_fasta), sys.argv[4])
  add_clusters(chromosome, p_fasta, sys.argv[1][-6], ranges[:len(ranges)/2], int(sys.argv[5]))
  add_clusters(chromosome, m_fasta, sys.argv[2][-6], ranges[len(ranges)/2:], int(sys.argv[5]))


if __name__ == '__main__':
  main()
