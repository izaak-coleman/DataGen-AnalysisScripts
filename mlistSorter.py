import sys
import callFormater

def main():
  if len(sys.argv) != 2:
    print("Usage: <exe> <mlist>")
  mlist = callFormater.mlistToCalls(sys.argv[1])
  mlist = sorted(mlist,key=lambda x:x[1])
  with open(sys.argv[1],'w') as f:
    f.write('\n'.join(["%s\t%d\t%s\t%s" % (a,b,c,d) for a,b,c,d in mlist]) + '\n')

if __name__ == '__main__':
  main()
