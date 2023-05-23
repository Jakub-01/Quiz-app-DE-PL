import re
import os
import pandas as pd

#defining a function to get vocabulary from excel file
def get_file(file_name,column):
    #defining a list to store vocabulary
    output_list = []
    #defining a path to the file
    current_path = os.getcwd()
    filepath = os.path.join(current_path,file_name)
    worklist = pd.read_excel(filepath).iloc[:,column]
    #iterating over the list to strip it from unnecessary characters
    for index, value in worklist.iteritems():
        stripped_line = value.strip()
        stripped_line = re.sub(r'\([^)]*\)', '', stripped_line)
        line_list = re.split(r"[{},;/\s]+",stripped_line)
        line_list = list(filter(lambda x: x != '', line_list))
        output_list.append(line_list)
    #returning the list
    return output_list
            


