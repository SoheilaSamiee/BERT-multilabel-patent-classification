# parsing us patents
# patent should be downloaded from: https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/
# This code is Inspired by https://github.com/lettergram/parse-uspto-xml

import pprint
import os
import sys
import html
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import csv
import re

# ---------------------------------------------------------------------------
# Function 
# ---------------------------------------------------------------------------
def parse_patent(bs):
    """
    Parses a US patent in a BeautifulSoup object.
    Only keeping the elements useful for our next text classification task
    """
    
    publication_title = bs.find('invention-title').text
    application_type = bs.find('application-reference')['appl-type']

    # International Patent Classification (IPC) Docs:
    sections = {}
    for classes in bs.find_all('classifications-ipcr'):
        for el in classes.find_all('classification-ipcr'):
            section = el.find('section').text                            
            sections[section] = True
    #print(list(sections.keys()))
    section_list = list(sections.keys())
    section_string =",".join(section_list)
        
    regex = re.compile('[^a-zA-Z]')  # remove all but alphabetic (even numbers -- change to '[^a-zA-Z0-9]' to keep numbers)
    
        
    abstracts = ''
    for el in bs.find_all('abstract'):
        abstracts += el.text.strip('\n')
        abstracts = regex.sub(' ', abstracts)
        abstracts = re.sub(r'\b\w{1,2}\b', '', abstracts)  # remove words of length < 3

    
    descriptions = ''
    for el in bs.find_all('description'):
        descriptions += el.text.strip('\n')
        descriptions = regex.sub(' ', descriptions)
        descriptions = re.sub(r'\b\w{1,2}\b', '', descriptions)  # remove words of length < 3

    
    claims = ''
    for el in bs.find_all('claim'):
        claims += el.text.strip('\n')
        claims = regex.sub(' ', claims)
        claims = re.sub(r'\b\w{1,2}\b', '', claims)  # remove words of length < 3
        #print(claims)
    
    # output in the dictionary format
    uspto_patent = {
        "sections": [section_string], 
        "publication_title": regex.sub(' ', publication_title.replace("\n"," ")),
        "application_type": regex.sub(' ', application_type.replace("\n"," ")),
        "abstract": abstracts.replace("\n"," "), 
        "descriptions": descriptions.replace("\n"," "), 
        "claims": claims.replace("\n"," ")
    }        

    return uspto_patent
# ---------------------------------------------------------------------------




# input file:
filenames = '../data/ipg210105.xml'

print('Start ...')    
all_patents = pd.DataFrame()
n_file = 1
count = 1
success_count = 0
errors = []

print("Filename:", filenames)
print("\n--------------------------------------------------------\n")

xml_text = html.unescape(open(filenames, 'r').read())

for patent in xml_text.split("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"):
    
    if patent is None or patent == "":
        print('No Patent')
        continue

    bs = BeautifulSoup(patent)

    # Skip documents which do not have classification-ipcr
    if bs.find('classification-ipcr') is None:
        #print('No classification!')
        continue 

    application = bs.find('us-patent-application')
    if application is None: # If no application, search for grant
        application = bs.find('us-patent-grant')

        
    # Setting the title
    title = "None"
    try:
        title = application.find('invention-title').text
    except Exception as e:          
        print("Error", count, e)

    # parsing the patent
    try: 
        uspto_patent = parse_patent(application)       
        new_patent = pd.DataFrame.from_dict(data=uspto_patent)
        
        if all_patents.empty:
            all_patents = new_patent            
        else:
            frames = [all_patents, new_patent]
            all_patents = pd.concat(frames)                
        success_count += 1
    except Exception as e:
        exception_tuple = (count, title, e)
        errors.append(exception_tuple)

    if (success_count+len(errors)) % 50 == 0:
        print(count, filenames, title)
        #new_patent.describe()
    count += 1

#print("\n\nErrors\n------------------------\n")
#for e in errors:
#    print(e)
    
print("Success Count:", success_count)
print("Error Count:", len(errors))

all_patents.to_csv('../data/all_patents_ipg210105.csv', index=False)

