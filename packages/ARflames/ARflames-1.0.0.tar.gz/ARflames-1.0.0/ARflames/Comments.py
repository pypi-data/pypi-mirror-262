import ARflames.FLAMES as fl
import ARflames.Split as sp
from ARflames.gui import *
import sys
def comments():
    ins="""
    This Is Fun Game Flames Game

    \n GE --- getnames , its gets inputs on  run time .
    \n SE --- setnames , its sets inputs on cmd .
    \n UI --- GUI , its show GUI Application .

    Prediction Means

    FLAMES :
      -- Friends
      -- Love
      -- Affection
      -- Marriage
      -- Enemy
      -- Sibilings
    """
    len1=len(sys.argv)
    #print(sys.argv)
    #print(len1)
    if len1==1:
        print(ins)
    else:
        match(sys.argv[1]):
            case "GE":
                    a=input("Enter The Name 1:")
                    b=input("Enter The Name 2:")
                    s=fl.times(sp.setnames(a,b))
                    print(s)
            case "SE":
                try:
                        s=fl.times(sp.setnames(sys.argv[2],sys.argv[3]))
                        print(s)
                except:
                      print("\n \t\tWrong Comments\n"+ins)
            case "UI":
                    UI()
            case _:
                    print(ins)

if __name__=='__main__':
    comments()
