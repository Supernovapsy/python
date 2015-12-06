import os
import subprocess
import argparse
import string
import glob

# caps and space to no caps and underscore.
def convert(input_string, lower = True):
    if lower:
        input_string = input_string.lower()
    trans_table = string.maketrans(' ', '_')
    return string.translate(input_string, trans_table)

def linuxfy(entry_path):
    if not os.path.lexists(entry_path):
        raise Exception("Path does not exist.")
    entry = os.path.basename(entry_path)
    entry_new = convert(entry, not args.retain_case)
    if entry != entry_new:
        response = raw_input("Rename " + entry + " to " + entry_new + "? ")
        if response.lower() == 'y' or response.lower() == 'yes':
            entry_path_old = os.path.abspath(entry_path)
            entry_path_par = os.path.join(entry_path, os.path.pardir)
            entry_path_new = os.path.join(os.path.abspath(entry_path_par), entry_new)
            command = 'mv "%s" "%s"' % (entry_path_old , entry_path_new)
            #print "command:", command # Debug
            retcode = subprocess.call(command, shell=True)
            if retcode == 0:
                print "Renamed", entry, "to", entry_new
            else:
                print "Return code", retcode, ", process stopped."
                print "Failing command is %s" % command
                exit()

def main(args):
    from sys import platform as _platform
    if not (_platform == "linux" or _platform == "linux2" or _platform == "darwin"):
        print "Need Unix shell environment"
        exit()

    unique_paths = dict.fromkeys(path for unix_path in args.paths for path in glob.iglob(unix_path)).keys()

    if args.recursive:
        for path in unique_paths:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    linuxfy(os.path.join(dirpath, filename))
                for dirname in dirnames:
                    linuxfy(os.path.join(dirpath, dirname))
    else:
        for path in unique_paths:
            linuxfy(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert files and directories to linux-style naming")
    parser.add_argument("paths", nargs="+", help="Files paths to which linux-style naming will be applied.")
    parser.add_argument("-r", "--recursive", help="convert to linux-style all files inside the paths given.", action='store_true')
    parser.add_argument("-c", "--retain_case", help = "Retain the case of entry names when converting.")

    args = parser.parse_args()

    main(args)
