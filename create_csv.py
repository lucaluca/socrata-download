# -*- coding: utf-8 -*-
# jgiuffrida, u chicago
# 8/5/14

import json
import os
import re

portal = 'opendata.bristol.gov.uk'  # the root URL of the portal without https://
outfile = 'metatable-bristol.txt'  # metatable-humanname.txt
numfiles = 19  # number of files in /searches

os.chdir('data/' + portal)


# do not include filters, maps, charts, calendars, or external links
matches = []
for f in range(1,numfiles+1):
    page = open('searches/' + str(f)).read()
    page_matches = re.findall('class="type typeFilter"[\s\S]*?rel=""', page)
    page_matches += re.findall('class="type typeMap"[\s\S]*?rel=""', page)
    page_matches += re.findall('class="type typeChart"[\s\S]*?rel=""', page)
    page_matches += re.findall('class="type typeCalendar"[\s\S]*?rel=""', page)
    page_matches += re.findall('class="type typeHref"[\s\S]*?rel=""', page)
    for match in page_matches:
        m = re.findall('/[a-z,0-9]{4}-[a-z,0-9]{4}" rel=""',match)[0][1:10]
        matches.append(m)


# function to remove unicode characters (occasionally need to add one)
def kill_unicode(s):
    s = s.replace(u'\u201d', '"')
    s = s.replace(u'\u201c', '"')
    s = s.replace(u'\u2013', "-")  
    s = s.replace(u'\u2010', "-")  
    s = s.replace(u'\u2014', "-")  
    s = s.replace(u'\u2018', "'")            
    s = s.replace(u'\u2019', "'")
    s = s.replace(u'\u2022', "-")
    s = s.replace(u'\u2020', "")
    s = s.replace(u'\xa0', "")
    s = s.replace(u'\xa3', "")
    s = s.replace(u'\xa7', "")
    s = s.replace(u'\xb7', "")
    s = s.replace(u'\xb0', '')
    s = s.replace(u'\xb2', '')
    s = s.replace(u'\xb3', '')    
    s = s.replace(u'\xb9', '')
    s = s.replace(u'\xb6', '')
    s = s.replace(u'\xe9', '')
    s = s.replace(u'\xe2', '')
    s = s.replace(u'\x80', '')
    s = s.replace(u'\x93', '')
    s = s.replace('\t', '    ')
    s = s.replace('\n', '')    
    s = s.replace('\r', '')    
    s = s.replace(u'\ufeff', '')
    return s


with open(outfile, 'w') as file:
    line = 'name\turl\tdisplay type\tview type\trecord count\tunique id\t' +\
        'temporal field\tlocation field\tupdate frequency\tcolumn names\t' +\
        'column count\tcategory\tdescription\ttags\ttime period\tgeocoded\n'
    file.write(line)
    i = 1
    viewids = open('viewids').read().split('\n')
    for viewid in viewids:
        if viewid in matches:  # derivative view
            continue
        view = open('views/' + viewid).read()
        try:
            data = json.loads(view)
        except:
            continue
        
        data_id = data['id']
        name = kill_unicode(data['name'])
        url = 'http://' + portal + '/resource/' + viewid
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
            unique_id = ''
            numRows = -1
            location = ''
            geocoded = 'no'
            temporal = ''
            if numColumns:
                try:
                    numRows = data['columns'][0]['cachedContents']['non_null'] + \
                    data['columns'][0]['cachedContents']['null']
                except KeyError: 
                    numRows = -1
                location = ''
                geocoded = 'no'
                temporal = ''
                try:
                    for col in range(0,numColumns):
                        if data['columns'][col]['dataTypeName'] == 'location':
                            location = data['columns'][col]['name']
                            geocoded = 'yes'
                        if data['columns'][col]['dataTypeName'] == 'calendar_date':
                            temporal = data['columns'][col]['name']
                        colNames += data['columns'][col]['name'] + ', '
                    for col in range(0,numColumns):
                        if location == '' and \
                            (data['columns'][col]['fieldName'] == 'latitude' or 
                            data['columns'][col]['fieldName'] == 'longitude' or 
                            data['columns'][col]['fieldName'] == 'Latitude' or 
                            data['columns'][col]['fieldName'] == 'Longitude'):
                            location = 'lat-long'
                            geocoded = 'yes'
                    for col in range(0,numColumns): 
                        if location == '' and \
                            (data['columns'][col]['fieldName'] == 'x_coordinate' or 
                            data['columns'][col]['fieldName'] == 'y_coordinate' or 
                            data['columns'][col]['fieldName'] == 'X' or 
                            data['columns'][col]['fieldName'] == 'Y'):
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
        unique_id = ''
        try:
            timePeriod = data['metadata']['custom_fields']['Metadata']['Time Period']
            timePeriod = kill_unicode(timePeriod)
        except KeyError: 
            timePeriod = ''
        try:
            updateFrequency = data['metadata']['custom_fields']['Metadata']['Frequency']
            updateFrequency = kill_unicode(updateFrequency)
        except KeyError: 
            try:
            	updateFrequency = data['metadata']['custom_fields']['Department Metrics']['Frequency']
            	updateFrequency = kill_unicode(updateFrequency)
            except KeyError:
            	updateFrequency = ''
        try:
            tags = json.dumps(data['tags'])[1:-1]
            tags = kill_unicode(tags)
        except KeyError: 
            tags = ''
        
        name = kill_unicode(name)
        temporal = kill_unicode(temporal)
        location = kill_unicode(location)
        updateFrequency = kill_unicode(updateFrequency)
        colNames = kill_unicode(colNames)
        category = kill_unicode(category)
        description = kill_unicode(description)
        tags = kill_unicode(tags)
        timePeriod = kill_unicode(timePeriod)
        
        
        line = name + '\t' + url + '\t' + displayType + '\t' + viewType + '\t' + \
            str(numRows) + '\t' + unique_id + '\t' + temporal + '\t' + \
            location + '\t' + updateFrequency + '\t' + colNames + '\t' + \
            str(numColumns) + '\t' + category + '\t' + description + '\t' + tags + \
            '\t' + timePeriod + '\t' + geocoded + '\n'
        file.write(line)
        print('view ' + str(i) + ' of ' + str(len(viewids)))
        i += 1

