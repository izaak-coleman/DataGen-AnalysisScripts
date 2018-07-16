import sys
import random
from subprocess import check_output

def randomClusterAdder(fastaName, nClusters, clustSize, dist):
  fasta = []
  dist = int(dist)
  clustSize = int(clustSize)
  nClusters = int(nClusters)
  print("Opening fasta...")
  with open(fastaName) as f:
    fasta = [l.strip() for l in f]
    fasta.pop(0)
    fasta = list("".join(fasta))
  mutationList = []
  clusters = []
  print("Entering cluster add loop")
  for i in range(nClusters):
    print i
    while True:
      newClust = random.randint(0,len(fasta))

      # try new location if clustLeft in centromere
      with open('/data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/snv.bed', 'w') as f:
        f.write('chr22\t%d\t%d\n' % (newClust, newClust+(clustSize*dist)))
      bedRes = check_output(['/data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier//bedtools2/bin/bedtools intersect -v -a /data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/snv.bed -b /data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/centromeres.bed'],shell=True)
      if bedRes == '':
        print "Failed SNV %d" %(newClust)
        continue
      else:
        print "Accepted SNV %d" %(newClust)

      # if clust beyond string length, continue
      if newClust+(clustSize*dist) >= len(fasta):
        continue
      # if already added, continue
      if inCluster(newClust, clusters):
        continue

      # check that mutations are not in N
      inN=False
      for i in range(newClust, newClust+clustSize*dist, dist):
        if fasta[i] == 'N':
          inN = True
      if inN:
        continue
      # location good, add cluster
      clusters.append((newClust, newClust+clustSize*dist,))
      for i in range(newClust, newClust+clustSize*dist, dist):
        if (i % 2):
          mutationList.append((i, fasta[i], transversion_mutation(fasta[i]),))
        else:
          mutationList.append((i, fasta[i], transition_mutation(fasta[i]),))
      break

  # finished adding SNV clusters
  for s,n,m in mutationList:
    fasta[s] = m

  return "".join(fasta), sorted(mutationList, key=lambda x:x[0])


def inCluster(newClust, clusters):
  for r,l in clusters:
    if newClust in range(l,r):
      return True
  return False


def randomSNVAdder(chromosome, fastaName, nMuts):
  fasta = ""
  with open(fastaName) as f:
    fasta = fasta.join([l.strip() for l in f if '>' not in l])
    fasta = list(fasta)
  mutationList = []

  for i in range(int(nMuts)):
    snv = ()
    while True:
      snvSite = random.randint(0, len(fasta))
      if (snvSite % 2):
        snv = (snvSite, fasta[snvSite], transversion_mutation(fasta[snvSite]))
      else:
        snv = (snvSite, fasta[snvSite], transition_mutation(fasta[snvSite]))
      # call bed to make sure SNV is outside of centromere
      with open('/data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/snv.bed', 'w') as f:
        f.write(chromosome + '\t%d\t%d\n' % (snv[0], snv[0]))
      bedRes = check_output(['/data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/bedtools2/bin/bedtools intersect -v -a /data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/snv.bed -b /data/ic711/WriteUp_analyses/results/tools/art_bin_MountRainier/centromeres.bed'],shell=True)
      if bedRes == '':
        print "Failed SNV %d" %(snv[0])
      if snv not in mutationList and snv[2] != 'N' and bedRes != '':
        break

    mutationList.append(snv)
  for snv in mutationList:
    fasta[snv[0]] = snv[2]
  return "".join(fasta), sorted(mutationList, key=lambda x:x[0])

def writeFastq(header, fasta, ofname, lineLength):
  of = open(ofname, 'w')
  of.write(header + '\n')
  out = '\n'.join([fasta[i:i+int(lineLength)] for i in range(0, len(fasta), int(lineLength))])
  of.write(out)
  of.close()

def writeSNVs(snvList, ofname, chromosome):
  of  = open(ofname, 'w')
  of.write('\n'.join(
    ["PointMutation\t%s\t%d\t%s\t%s" % (chromosome, site+1, h, t) for site, h, t in snvList]
  ) + '\n')
  of.close()

def transversion_mutation(base):
    return {
        "A":"T",
        "T":"A",
        "C":"G",
        "G":"C",
        "N":"N"
    }[base]

def transition_mutation(base):
    return {
        "A":"G",
        "G":"A",
        "T":"C",
        "C":"T",
        "N":"N"
    }[base]

def main():
  if len(sys.argv) != 7:
    print "Usage: <exe> <fa> <nmuts> <o_fa_name> <line_len> <o_m_list_name> <chromosome> "
    sys.exit(1)

  fasta, mutationList = randomSNVAdder(sys.argv[6], sys.argv[1], sys.argv[2])
  f=open(sys.argv[1])
  writeFastq(f.readlines()[0], fasta, sys.argv[3], sys.argv[4])
  f.close()
  writeSNVs(mutationList, sys.argv[5], sys.argv[6])

if '__main__' == __name__:
  main()
