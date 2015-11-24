import csv
from sys import argv
import unittest
import re
import subprocess

######### TESTS ########

class TestProgram(unittest.TestCase):
    judgeN = 35

    def test_csv_judges(self):
        judges = get_judges(table)
        self.assertEqual(len(judges), self.judgeN)

######## FUNCTIONS #####

# Remove duplicates in a vector
def remove_duplicates(vector):
    # Create a dictionary to do this O(n) time.
    unique_elements = dict()
    for i in vector:
        # The dictionary keys will always only have unique elements.
        unique_elements.setdefault(i)
    return list(unique_elements)

# Note that this is hardcoded right now to get the judges' cells.
# There is no way around this because currently there are no rules
# on the format of the judges' assignment table and so no code can
# be written to test for that.
def get_judges(table):
    judges = list()
    judge_rows = table[6:10] + table[17:21]
    for row in judge_rows:
        for entry in row:
            judge_name = search_judge_name(entry)
            if judge_name:
                judges.append(judge_name)
    judges = remove_duplicates(judges)
    # print judges # debug
    return judges

def search_judge_name(entry):
    #print entry # debug
    # TO IMPROVE: Of course this doesn't catch corner cases.
    search = re.search('[a-z,A-Z]+ ?\.[a-z,A-Z, ,\-]+', entry)
    if search:
        return search.group(0) # Return the matched string.
    else:
        return False

# Input: table from excel sheet
# Output: array [MC, alias, pres_key, [judges]]
def get_initial_db_entry(subtable):
    entry = list()
    entry.append(subtable[0]) # MC
    entry.append(subtable[2]) # alias
    if re.search('BA', subtable[1]):
        entry.append('podium')
    else:
        entry.append('poster')
    entry.append(list()) # This array is element 3.

    for cell in subtable[3:]:
        name = search_judge_name(cell)
        if name:
            entry[3].append(name)
    # print entry # Debug
    return entry

def get_array_col(array, col):
    return [row[col] for row in array]

# Input: entire raw excel table
# Output: Initial databse.
def get_initial_db(table):
    initial_db = list()

    poster_cols = range(1, 7)
    #podium_cols = range(1, 5) + range(6, 10)
    podium_cols = range(1, 9)
    poster_row_ends = [3, 10]
    podium_row_ends = [14, 21]
    poster_subtable = table[poster_row_ends[0]:poster_row_ends[1]][:]
    podium_subtable = table[podium_row_ends[0]:podium_row_ends[1]][:]
    for i in poster_cols:
        session = get_array_col(poster_subtable, i)
        initial_db.append(get_initial_db_entry(session))
    for i in podium_cols:
        session = get_array_col(podium_subtable, i)
        initial_db.append(get_initial_db_entry(session))

    return initial_db

# Input: initial database of entries.
# Output: Final database as a dict with professors as the keys and
# the MC, category name, and presentation type (in that order) to be retrieved in an array,
# which at most contains 2 elements for the two types of presentations.
# {judge: [MC, session type, presentation type]}
def convert_initial_db(db_init):
    judge_data = dict()
    for session in db_init:
        for judge in session[3]:
            judge_info_value_new = [session[0], session_names[session[1]][0], session[2]]
            if judge_data.has_key(judge):
                judge_info_value_list = judge_data.get(judge)
                judge_info_value_list = judge_info_value_list.append(judge_info_value_new)
            else:
                judge_info_value_list = [judge_info_value_new]
            judge_data.setdefault(judge, judge_info_value_list)
            # print "session: %r" % session
            # print "updating %s with" % judge
            # print judge_info_value_new
    return judge_data

def substitute_email(email, judge_name, judge_info):
    if len(judge_info) == 0 or len(judge_info) > 2:
        raise Exception("judge_info doesn't have the correct correct length. A judge can only judge one or two sessions.")
    email = email.replace('[judge_name]', judge_name)
    email = email.replace('[MC_name_1]', judge_info[0][0])
    email = email.replace('[category_name_1]', judge_info[0][1])
    email = email.replace('[presentation_type_1]', judge_info[0][2])
    if len(judge_info) == 2:
        email = email.replace('(', '')
        email = email.replace(')', '')
        email = email.replace('[MC_name_2]', judge_info[1][0])
        email = email.replace('[category_name_2]', judge_info[1][1])
        email = email.replace('[presentation_type_2]', judge_info[1][2])
    else:
        email = email.replace(re.search('\(.+\)', email).group(0), '')
    return email

######### MAIN #########

script, fileName = argv

# Podium, then poster (if exists) letterings are appended
session_names = {
    "Chemical"      : ["Chemical", ['M', 'I']],
    "Bio"           : ["Biomedical", ['A', 'G']],
    "Mechanical"    : ["Mechanical & Aerospace", ['B', 'J']],
    "ECE"           : ["Electrical & Computer", ['C', 'E']],
    "Material"      : ["Materials", ['L', 'F']],
    "Industrial"    : ["Industrial", ['K']],
    "CEI"           : ["Civil, Environmental, & Industrial", ['H']],
    "Civ/Enviro"    : ["Civil & Environmental", ['D']],
    "Bio/Comp"      : ["Bioelectrical & computer", ['N']]
}

#fileName = "general_task.csv"

# Read the contents of the file into the table.
table = list() # a list of rows of the csv input file.
with open(fileName, 'r') as infoFile:
    reader = csv.reader(infoFile, delimiter=',', quotechar='"')
    for row in reader:
        table.append(row)

########### CODE ################3

initial_db = get_initial_db(table)
judge_data = convert_initial_db(initial_db)
#print judge_data

email_template = open("last_email_template.txt", 'r').read()

if subprocess.call("mkdir emails", shell=True) == 1:
    raise Exception("Cannot make directory 'emails'")

for judge_name, judge_info in judge_data.iteritems():
    email = open("emails/" + judge_name, 'w')
    email.write(substitute_email(email_template, judge_name, judge_info))
    email.close()

print "All emails written"

############ TEST ###############3

#   print table # Debug

if __name__ == "__main__":
    del argv[1:]
    unittest.main()