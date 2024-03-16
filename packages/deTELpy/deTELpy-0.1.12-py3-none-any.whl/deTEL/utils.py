import os


def is_valid_file(p, arg):
    if not os.path.exists(arg):
        p.error("The file %s does not exist!" % arg)
    else:
        return arg


def prep_folder(arg):
    if not os.path.exists(arg):
        os.mkdir(arg)

    return arg
