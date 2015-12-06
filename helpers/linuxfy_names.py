import os
import subprocess
import argparse

# caps and space to no caps and underscore.
def convert(input_string):
    return "_".join(input_string.lower().split())

def linuxfy(entry_path):
    # Get the actual entry's name out of the whole path.
    if entry_path[-1] == '/':
        entry_path = entry_path[:-1]
    entry_split = entry_path.rsplit('/', 1)
    entry = entry_split[1]
    entry_new = convert(entry)
    if entry != entry_new:
        response = raw_input("Rename " + entry + " to " + entry_new + "? ")
        if response.lower() == 'y' or response.lower() == 'yes':
            entry_path_new = os.path.join(entry_split[0], entry_new)
            command = 'mv "%s" "%s"' % (entry_path, entry_path_new)
            #print "command:", command # Debug
            retcode = subprocess.call(command, shell=True)
            if retcode == 0:
                print "Renamed", entry, "to", entry_new
            else:
                print "Return code", retcode, ", process stopped."
                print "Failing command is %s" % command
                exit()

def main(args):
    if args.file_paths[0] == '*':
        file_paths = os.listdir('.')
    else:
        file_paths = args.file_paths

    if args.recursive:
        for path in file_paths:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    linuxfy(os.path.join(dirpath, filename))
                for dirname in dirnames:
                    linuxfy(os.path.join(dirpath, dirname))
    else:
        for file in file_paths:
            linuxfy(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert files and directories to linux-style naming")
    parser.add_argument("file_paths", nargs="+", help="Files paths to which linux-style naming will be applied.")
    parser.add_argument("-r", "--recursive", help="convert to linux-style all files inside the paths given.", action='store_true')

    args = parser.parse_args()

    main(args)
