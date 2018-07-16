import sys

def SNV_results_to_vcf(fname):
  base = fname[:-12]
  calls = []
  with open(fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls.pop(0)
    calls = [[a,b,int(convert(c[3:])),int(d),e,f] for a,b,c,d,e,f in calls]
    calls = sorted(calls, key=lambda x: (x[2], x[3]))
  vcf = '\n'.join(['\t'.join([str(convert(e[2])), str(e[3]), e[0], e[4], e[5], '.', 'PASS', e[1]]) for e in calls])
  vcf = '\t'.join("#CHROM POS ID REF ALT QUAL FILTER INFO".split()) + '\n' + vcf
  return vcf

def convert(e):
  if   e == 'X': return 23
  elif e == 'Y': return 24
  elif e == 23 : return 'X'
  elif e == 24 : return 'Y'
  else:          return e

def main():
  if len(sys.argv) != 2:
    print ("Usage <exe> <SNV_results>")
    sys.exit(1)
  base = sys.argv[1][:-12]
  with open (base + '.vcf', 'w') as f:
    f.write(SNV_results_to_vcf(sys.argv[1]))

if '__main__' == __name__:
    main()
