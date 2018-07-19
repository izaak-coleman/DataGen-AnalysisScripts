
def mutectToCalls(fname):
  with open(fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls = [(e[0], int(e[1]), e[3], e[4]) for e in calls]
  return calls

def gediToCalls(fname):
  with open(fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls = [(e[2], int(e[3]), e[4], e[5]) for e in calls]
  return calls

def mlistToCalls(fname):
  with open(fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls = [(e[1], int(e[2]), e[3], e[4]) for e in calls]
  return calls

def vcfToCalls(fname):
  with open(fname) as f:
    calls = [l.strip().split('\t') for l in f]
    calls = [('chr'+e[0], int(e[1]), e[3], e[4]) for e in calls]
    return calls
