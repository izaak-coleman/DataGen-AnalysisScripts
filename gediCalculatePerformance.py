# -*- coding: utf-8 -*-
import sys

def generateSNPList(fname):
  snp_list  = []
  with open(fname) as f:
    snp_list = [l.strip().split('\t') for l in f]
    snp_list = [(l[0], l[2], l[7].split('/')) for l in snp_list]
  return snp_list

def generateSNVList(fname):
    snv_list = []
    with open(fname) as f:
      snv_list = [l.strip().split('\t') for l in f]
      snv_list = [(l[1],l[2], l[3], l[4]) for l in snv_list]
    return snv_list

def  generateCallsList(fname):
  calls = []
  with open(fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls.pop(0)
    calls = [(l[2], l[3], l[4], l[5]) for l in calls]
  return calls

def hitSNVs(calls, snvs):
  hit_snvs = []
  for snv in snvs:
    for call in calls:
      if call == snv:
        hit_snvs.append(call)
  return hit_snvs

def hitSNPs(calls, snps):
  hit_snps = []
  for call in calls:
    for snp in snps:
      if call[0] == snp[0] and call[1] == snp[1] and call[3] in snp[2]:
        hit_snps.append(call)
  return hit_snps

def main():
  if len(sys.argv) != 6:
    print("Usage: <exe> <m_snv> <p_snv> <m_snp> <p_snp> <calls>")
    sys.exit(1)
  snvs = generateSNVList(sys.argv[1]) + generateSNVList(sys.argv[2])
  snps = generateSNPList(sys.argv[3]) + generateSNPList(sys.argv[4])
  calls = generateCallsList(sys.argv[5])
  hit_snps = hitSNPs(calls, snps)
  hit_snvs = hitSNVs(calls, snvs)

  Calls = "n Calls: " + str(len(calls))
  SNVs = "n hit_SNVs: " + str(len(hit_snvs))
  r = float(len(hit_snvs)) / len(snvs) 
  p = (float(len(hit_snvs)) / len(calls))  
  Recall = "Recall: " + str(  (float(len(hit_snvs)) / len(snvs))  )
  Precision = "Prec: " + str(  (float(len(hit_snvs)) / len(calls))  )
#print(Calls)
#  print(SNVs)
  print("n hit_SNPs: " + str(len(hit_snps)))
  print("Prec snpfil: " + str(  (float(len(hit_snvs)) / (len(calls)-len(hit_snps))) ))
#  print(Recall)
#  print(Precision)
  print(','.join([str(len(hit_snvs)), str(len(calls)), "AF", "Caller", str(r), str(p)]))

if __name__ == "__main__":
  main()
