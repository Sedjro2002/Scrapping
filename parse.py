import json
import pandas as pd
import ast
import re
from pathlib import Path

def correctSingleQuoteJSON(s):
    rstr = ""
    escaped = False

    for c in s:
    
        if c == "'" and not escaped:
            c = '"' # replace single with double quote
        
        elif c == "'" and escaped:
            rstr = rstr[:-1] # remove escape character before single quotes
        
        elif c == '"':
            c = '\\' + c # escape existing double quotes
   
        escaped = (c == "\\") # check for an escape character
        rstr += c # append the correct json
    
    return rstr


print('debut du script')
# with open("donnees_brutes.json", "r") as f:   
#     data = correctSingleQuoteJSON(f.read())
#     data = f.read().strip()
#     l = eval(data)    
#     parsed_data = json.dumps(l)
# Path('donnees_brutes2_corrigees.json').write_text(parsed_data)
#     print('debut du televersement des donnees...')
#     data = json.load(f)
#     print('donnees televersees')

# print('debut de la conversion en dataframe...')
# df = pd.DataFrame(parsed_data)
# print('donnees converties en dataframe')

# print('debut de la conversion en excel...')
# df.to_excel("donnees_brutes_excel.xlsx")
# print('fin de la conversion')





def getJson(filepath):
    fr = open(filepath, 'r')
    lines = []
    for line in fr.readlines():
        line_split = line.split(",")
        set_line_split = []
        for i in line_split:
            i_split = i.split(":")
            i_set_split = []
            for split_i in i_split:
                set_split_i = ""
                rev = ""
                i = 0
                for ch in split_i:
                    if ch in ['\"','\'']:
                        set_split_i += ch
                        i += 1
                        break
                    else:
                        set_split_i += ch
                        i += 1
                i_rev = (split_i[i:])[::-1]
                state = False
                for ch in i_rev:
                    if ch in ['\"','\''] and state == False:
                        rev += ch
                        state = True
                    elif ch in ['\"','\''] and state == True:
                        rev += ch+"\\"
                    else:
                        rev += ch
                i_rev = rev[::-1]
                set_split_i += i_rev
                i_set_split.append(set_split_i)
            set_line_split.append(":".join(i_set_split))
        line_modified = ",".join(set_line_split)
        lines.append(ast.literal_eval(str(line_modified)))
    return lines
lines = getJson('donnees_brutes2.json')
for i in lines:
    Path('donnees_brutes2_corrigees.json').write_text(str(i))
