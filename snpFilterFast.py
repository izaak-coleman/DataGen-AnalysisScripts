import sys

def snpFilter(snp_fname, calls_fname):
  snps = []
  calls = []
  snp_site = []
  var_dict = {}
  with open(snp_fname) as f:
    snps = [l.strip().split('\t') for l in f]
    snp_site = [(e[0], e[1]) for e in snps]
    for i in range(0,len(snp_site)):
      var_dict[snp_site[i][0] + snp_site[i][1]] = snps[i][7].split('/')

  with open(calls_fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls.pop(0)
  snp_filtered_calls = []
  snp_removed = []
  for call in calls:
    if not snp(call, snp_site, var_dict):
      snp_filtered_calls.append('\t'.join(call))
    else:
      snp_removed.append('\t'.join(call))
  with open(calls_fname+'.snp_fil','w') as f:
    f.write('\n'.join(snp_filtered_calls))
  with open(calls_fname+'.snp_rem','w') as f:
    f.write('\n'.join(snp_removed))

def snp(call, snp_site, var_dict):
  _,_,c,pos,h,t = call
  return ((c,pos) in snp_site) and ((h in var_dict[c+pos]) and (t in var_dict[c+pos]))

def main():
  if len(sys.argv) != 3:
    print("Usage: <exe> <snp_file> <calls_file>")
    sys.exit(1)
  snpFilter(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
  main()
