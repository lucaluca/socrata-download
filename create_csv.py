# -*- coding: utf-8 -*-
# jgiuffrida, u chicago
# 8/5/14

import json
import os
import re

path = "/Users/jcgiuffrida/Documents/tech/git/socrata-download/data/datacatalog.cookcountyil.gov"
%cd "/Users/jcgiuffrida/Documents/tech/git/socrata-download/data/datacatalog.cookcountyil.gov"


# id
# name
# display type
# view type
# time period
# num cols
# num rows
# description
# category
# update freq
# tags
# unique_id
# location
# geocoded
# temporal

# which views are derivative? filters, maps, and charts
matches = []
# replace '37' with number of files in /searches + 1
for f in range(1,37):
    page = open('searches/' + str(f)).read()
    page_matches = re.findall('class="type typeFilter"[\s\S]*?rel=""', page)
    page_matches += re.findall('class="type typeMap"[\s\S]*?rel=""', page)
    page_matches += re.findall('class="type typeChart"[\s\S]*?rel=""', page)
    for match in page_matches:
        m = re.findall('/[a-z,0-9]{4}-[a-z,0-9]{4}" rel=""',match)[0][1:10]
        matches.append(m)


# function to remove unicode characters
def kill_unicode(s):
    s = s.replace(u'\u201d', '"')
    s = s.replace(u'\u201c', '"')
    s = s.replace(u'\u2013', "-")  
    s = s.replace(u'\u2010', "-")  
    s = s.replace(u'\u2014', "-")  
    s = s.replace(u'\u2018', "'")            
    s = s.replace(u'\u2019', "'")
    s = s.replace(u'\u2022', "-")
    s = s.replace(u'\xb0', '')
    s = s.replace(u'\xb2', '')
    s = s.replace(u'\xb3', '')    
    s = s.replace(u'\xb9', '')
    s = s.replace('\t', '    ')
    s = s.replace('\n', '')    
    s = s.replace('\r', '')    
    return s


outfile = 'metatable-cook.txt'
with open(outfile, 'w') as file:
    line = 'id\tname\turl\tdisplay type\tview type\ttime period\tnumber of fields\t' +\
        'record count\tdescription\tcategory\tupdate frequency\ttags\tunique id\t' +\
        'location field\tgeocoded\ttemporal field\tcolumn names\n'
    file.write(line)
    i = 1
    viewids = open('viewids').read().split('\n')
    for viewid in viewids:
        if viewid in matches:  # derivative view
            continue
        view = open('views/' + viewid).read()
        data = json.loads(view)
        
        data_id = data['id']
        name = kill_unicode(data['name'])
        url = 'http://data.cityofchicago.org/resource/' + viewid
        try:
            description = data['description']
            description = kill_unicode(description)
        except KeyError:
            description = ''
        try:
            category = kill_unicode(data['category'])
        except KeyError: 
            category = ''
        try:
            displayType = data['displayType']
        except KeyError: 
            displayType = ''
        try:
            viewType = data['viewType']
        except KeyError:
            viewType = ''
        colNames = ''
        try: 
            numColumns = len(data['columns'])
            if numColumns:
                try:
                    numRows = data['columns'][0]['cachedContents']['non_null'] + \
                    data['columns'][0]['cachedContents']['null']
                except KeyError: 
                    numRows = -1
                    unique_id = ''
                try:
                    for col in range(0,numColumns):
                        if data['columns'][col]['cachedContents']['non_null'] == numRows:
                            unique_id = data['columns'][col]['name']
                            break
                except KeyError: 
                    pass
                location = ''
                geocoded = 'no'
                temporal = ''
                try:
                    for col in range(0,numColumns):
                        if data['columns'][col]['dataTypeName'] == 'location':
                            location = 'location'
                            geocoded = 'yes'
                        if data['columns'][col]['dataTypeName'] == 'calendar_date':
                            temporal = data['columns'][col]['name']
                        colNames += data['columns'][col]['name'] + ', '
                    for col in range(0,numColumns):
                        if location == '' and \
                            (data['columns'][col]['fieldName'] == 'latitude' or 
                            data['columns'][col]['fieldName'] == 'longitude'):
                            location = 'lat-long'
                            geocoded = 'yes'
                    for col in range(0,numColumns): 
                        if location == '' and \
                            (data['columns'][col]['fieldName'] == 'x_coordinate' or 
                            data['columns'][col]['fieldName'] == 'y_coordinate'):
                            location = 'x-y'
                            geocoded = 'yes'
                    for col in range(0,numColumns):
                        if location == '' and \
                            (data['columns'][col]['fieldName'] == 'zip' or 
                            data['columns'][col]['fieldName'] == 'address' or 
                            data['columns'][col]['fieldName'] == 'street_address'):
                            location = 'address'
                except KeyError: 
                    pass
        except KeyError: 
            numColumns = 0
            numRows = -1
            location = ''
            geocoded = 'no'
            temporal = ''
        colNames = kill_unicode(colNames)
        unique_id = kill_unicode(unique_id)
        try:
            timePeriod = data['metadata']['custom_fields']['Metadata']['Time Period']
            timePeriod = kill_unicode(timePeriod)
        except KeyError: 
            timePeriod = ''
        try:
            updateFrequency = data['metadata']['custom_fields']['Metadata']['Frequency']
            updateFrequency = kill_unicode(updateFrequency)
        except KeyError: 
            updateFrequency = ''
        try:
            tags = json.dumps(data['tags'])[1:-1]
            tags = kill_unicode(tags)
        except KeyError: 
            tags = ''
        
        line = data_id + '\t' + name + '\t' + url + '\t' + displayType + '\t' + \
            viewType + '\t' + \
            timePeriod + '\t' + str(numColumns) + '\t' + str(numRows) + '\t' + \
            description + '\t' + category + '\t' + updateFrequency + '\t' + \
            tags + '\t' + unique_id + '\t' + location + '\t' + geocoded + '\t' + \
            temporal + '\t' + colNames + '\n'
        file.write(line)
        print('view ' + str(i) + ' of ' + str(len(viewids)))
        i += 1

