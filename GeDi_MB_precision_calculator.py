import sys

def extract_gedi_snv_calls(fname):
  calls = []
  with open(fname) as f:
    calls = [l.strip().split('\t')  for l in f]
  calls.pop(0) # remove header
  return [(e[2][3:],int(e[3]), e[4], e[5]) for e in calls] # return (chromosome, pos, healthy, tumour) tuples

def extract_MB_gold_snvs(fname):
  snvs = []
  with open(fname) as f:
    snvs = [l.strip().split('\t') for l in f]
  return [(e[0], int(e[1]), e[3], e[4]) for e in snvs] # return (chromosome, pos, healthy, tumour) tuples

def calc_snv_intersection(calls, snvs):
  snvs_set = set(snvs)
  return [call for call in calls if call in snvs_set] # get intersection

def print_tuples(intersection):
  stringified_tups = ['\t'.join([c,str(p),h,t]) for c, p, h, t in intersection]
  print ('Chromosome\tPosition\tControl\tTumour\n' + '\n'.join(stringified_tups))

def main():
  if len(sys.argv) != 3:
    print("Usage: <exe> <goldSNVs> <GeDi_SNV_calls>")
    sys.exit(1)
  snvs = extract_MB_gold_snvs(sys.argv[1])
  calls = extract_gedi_snv_calls(sys.argv[2])
  intersection = calc_snv_intersection(calls, snvs)
  print_tuples(intersection)
  print("Precision: " + str( float(len(intersection)) / len(calls) ))

if '__main__' == __name__:
  main()
