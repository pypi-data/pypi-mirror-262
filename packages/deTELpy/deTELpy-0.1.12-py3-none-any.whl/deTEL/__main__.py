import sys

if __name__ == "__main__":
    from mTEL import mTEL
    from deTEL.eTEL.workflow.eTEL import ETelRunner
    from deTEL.rTEL.open_search import OpenSearchRunner
else:
    from .mTEL import mTEL
    from .eTEL import eTEL
    from .rTEL.open_search import OpenSearchRunner


mode = sys.argv[1:]
if len(mode) == 0:
    from deTEL.gui import GUIRunner

    GUIRunner().main()
    exit(1)
else:
    if mode[0] == "mTEL":
        mTEL.run(sys.argv[2:])
    elif mode[0] == "eTEL":
        ETelRunner().run(sys.argv[2:])
    elif mode[0] == "rTEL":
        OpenSearchRunner().run(sys.argv[2:])
    else:
        print("Argument error. Argument length: ", len(mode))
        exit(1)
