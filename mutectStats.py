import sys
def sensitivity(keeps, snvs):
  """Function takes the list of MuTect keeps, and the list of genuine SNVs
     Using this, the sensitivty of mutect is calculated:
     S = TP / TP + FN """
  # Format data
  snvs = [(int(snv.split('\t')[2]), snv.split('\t')[3], snv.split('\t')[4]) for snv in snvs]
  keeps = [(int(k.split('\t')[1]), k.split('\t')[3], k.split('\t')[4]) for k in keeps]

  # Remove duplicates
  snvs = list(set(snvs))
  keeps = list(set(keeps))

  # Sort on SNV location
  keeps = sorted(keeps, key=lambda x:x[0])
  snvs  = sorted(snvs,  key=lambda x:x[0])
  print len(snvs)

  # Extract called SNVs (TP)
  tp = [call for call in keeps if call in snvs]

  # compute sensitivity tp  / tp + fn
  return (len(tp) / float(len(snvs))), len(tp)


def precision(keeps, snvs):
  """Function takes the list of MuTect keeps and the list of genuine SNVs
     Using this, the precision of mutect is calculated:
     P = TP / TP + FP """
  # Format data
  snvs = [(int(snv.split('\t')[2]), snv.split('\t')[3], snv.split('\t')[4]) for snv in snvs]
  keeps = [(int(k.split('\t')[1]), k.split('\t')[3], k.split('\t')[4]) for k in keeps]

  # Remove duplicates
  snvs = list(set(snvs))
  keeps = list(set(keeps))

  # Sort on SNV location
  keeps = sorted(keeps, key=lambda x:x[0])
  snvs  = sorted(snvs,  key=lambda x:x[0])

  # Extract called SNVs (TP)
  tp = [call for call in keeps if call in snvs]

  # compute precision tp / tp + fp
  return (len(tp) / float(len(keeps))), len(keeps)

def main():
  """main(): Computes the sensitivity and precision of mutect keeps file, vs
    the list of known SNVs"""
  if len(sys.argv) != 3:
    print "Usage: <exe> <keeps> <snv>"
    print main.__doc__
    sys.exit(1)

  keeps = []
  snvs  = []
  with open(sys.argv[1]) as f:
    keeps = [l.strip() for l in f]

  with open(sys.argv[2]) as f:
    snvs  = [l.strip() for l in f]
  sens, prec, snv_hists, n_keeps  = 0,0,0,0

  try:
    sens, snv_hits = sensitivity(keeps, snvs)
  except ZeroDivisionError:
    pass

  try:
    prec, n_keeps = precision(keeps, snvs)
  except ZeroDivisionError:
    pass 

  print ",".join(["DS",str(snv_hits), str(n_keeps), "AF", "CL",str(sens), str(prec)])


if "__main__" == __name__:
  main()
