#! /usr/bin/python
# -*- coding: utf-8 -*-
import csv, os, time, re, codecs
import unicodedata

# Error-code meaning:
#   0 = OK
#   1 = Error when accessing DB-file
#   2 = The specific project ID doesn't exist
_error_code = 1
_error_meaning = ["Ok", "Something went wrong accessing the database. Please try again, or contact the webmaster.", "The project you're trying to access does not exist. Please choose another one"]

# _data will contain all the data from the CSV-database
_data = []
# _log will contain the logs
_log = []

# **** TODO ****
# Implement the error codes! - Done
# Comment the entire code - Done
# Implement the logging system - Done

def init():
    # This initiates the CSV-file that contains all the projects
    # It tries to open the CSV-file and if it fails it will set _error_code to 1

    global _error_code
    global _data

    _data = []

    try:
        # Open the CSV-file and get the fieldnames by reading the first line of the file
        # Loops through the entire file and adds all the values to the dictionary field
        # At the end all the fields' will be added to the list _data that will be used for the data
        _csv_reader = csv.reader(open("data.csv", "r"))
        _csv_fieldnames = _csv_reader.next()

        for row in _csv_reader:
            field = {}

            for fieldName in _csv_fieldnames:
                index = _csv_fieldnames.index(fieldName)
                
                if not row[index].isdigit():
                    if len(row[index]) == 0:
                        field[fieldName] = None
                    else:
                        field[fieldName] = unicode(row[index], "utf-8")
#unicode(row[index].encode("utf-8", "ignore"), "utf-8")
                else:
                    if len(row[index]) > 1:
                        field[fieldName] = str(row[index])
                    else:
                        field[fieldName] = int(row[index])
            _data.append(field)

        # Add the techniques to the specific project to a list and sort it
        for row in _data:
            if row["techniques_used"] != None:
                row["techniques_used"] = row["techniques_used"].split(",")
                row["techniques_used"].sort()
            else:
                row["techniques_used"] = []

        _error_code = 0
#        print _data
        _log.append("Called init() to initiated the database-file at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".\n")

    except IOError:
        _error_code = 1
        _log.append("Failed to initate the database-file with init() at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ". Error-code " + str(_error_code) + ".\n")

    # Calls the log-function so everything in _log is written to the log-file
    log()

def project_count():
    # Returns how many projects there are in _data (which contains all the projects)

    global _error_code
    global _data

    if _error_code == 0:
        _error_code = 0
        _log.append("Called project_count() at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".\n")
    else:
        _log.append("Failed to call project_count() at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "Error-code: " + str(_error_code) + "\n")
    log()

    return (_error_code, len(_data))

def lookup_project(id):
    # To get a specific project's details
    # Will return _proj as a dictionary, or as None

    global _error_code
    global _data

    _proj = {}
    if re.findall("[\d.]*\d+", id):
        _proj = [i for i in _data if int(i["project_no"]) == int(id)]
        _log.append("Called lookup_project(id) with id: " + str(id) + " at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".\n")
    else:
        _proj = None
        _log.append("Failed to call lookup_project(id) with id:" + str(id) + " at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ". Error-code: " + str(_error_code) + "\n")
        _error_code = 2

    log()

    return (_error_code, _proj)

def retrieve_projects(sort_by="start_date", sort_order="asc", techniques=[], search="", search_fields=[]):
    # Loop through all the projects in _data
    # Create another loop inside the first one that goes through all the techniques that are specified
    # It checks if that technique is in the current project's techniques list
    # If it doesn't exist it will not be in the final result

    global _error_code
    global _data

    _list = []

    # Start of "check what to look for"
    if isinstance(techniques, list) and len(techniques) > 0:
        _techs = techniques
    else:
        _techs = None

    if isinstance(search_fields, list) and len(search_fields) > 0:
        _fields = search_fields
    else:
        _fields = None
    
    if isinstance(search, str) and len(search) > 0:
        search = unicode(search, "utf-8")
    elif isinstance(search, unicode):
        search = search
    else:
        search = None

    # To search for a technique
    # Loop through _data
    # Loop through _techs (which holds which techniques to search for)
    # If the search-technique match the project-technique it will add the project to _list
    # 
    # If no techniques are specified to search for it will copy _data's content to _list
    if _techs != None:
        for rows in _data:
            for tech in _techs:
                # Won't work with >1 technique
                if tech in rows["techniques_used"] and len(rows["techniques_used"]) > 0:
                    _list.append(rows)
    else:
        _list = _data[:]
    
    # Creates a new list to add the data that are sorted out by the search criteria
    # 
    # If there aren't any new search criterias the new list will only get the data from _list
    _new_list = []

    if _fields != None:
        field = [x for x in _fields]
        for row in _list:
            for x in _fields:
                if search != None:
                    if type(row[x]) is not unicode:
                        row[x] = unicode(str(row[x]), "utf-8")
                    
                    if search.lower() in row[x].lower():
                        _new_list.append(row)
                        break
                else:
                    # Add everything to the new_list because no search string
                    _new_list = _list[:]


    '''
    The old
    if search != None:
        if _fields != None:
            for field in _fields:
                for row in _list:
                    r_string = row[field]
                    
                    if type(r_string) is not unicode:
                        r_string = unicode(str(r_string), "utf-8")

                    if search.lower() in r_string.lower():
                        _new_list.append(row)
                    ww += 1
        else:
            # Que?
            _error_code = 1
            # Need to look in all search_fields that exists
    else:
        _new_list = _list[:]
    # End of "check what to look for"
    '''
    # Checks to see if the search-result should be returned descending or ascending
    if isinstance(sort_order, str) and len(sort_order) > 0:
        if sort_order == "desc":
            _new_list = sorted(_new_list, key=lambda project: project[sort_by],reverse=True)
        else:
            _new_list = sorted(_new_list, key=lambda project: project[sort_by])

    # Checks to see if any criteriums have been specified
    if _techs is None and _fields is None and search is None:
        _log.append("Called retrieve_projects() without any arguments. Returned all the data from the CSV-database file at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n")
        _new_list = _data
    else:
        _log.append("Called retrieve_projects() with argument(s) at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n")
        _log.append("\t Argument(s): \n\t\t Techniques: " + str(_techs) + " \n\t\t Search fields: " + str(_fields) + " \n\t\t Search string: " + unicodedata.normalize("NFKD", search).encode("ascii", "ignore") + " \n\t\t Sorted by key: " + str(sort_by) + " \n\t\t Shown as: " + str(sort_order) + "\n")
    
    log()
    return (_error_code, _new_list)

def retrieve_techniques():
    # Name says it all..

    global _data
    global _error_code

    _list = []
    for rows in _data:
        _list.extend(rows["techniques_used"])
        
    _new_list = []
    for items in _list:
        if items not in _new_list:
            _new_list.append(items)

    _log.append("Called retrieve_techniques() at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".\n")
    log()
    _error_code = 0

    return (_error_code, sorted(_new_list))

def retrieve_technique_stats():
    # To get all the techniques used for the different projects. Have a counter to know how many times a certain tehnique have been used

    global _error_code
    global _data

    # Creates a list for the data
    _list = []

    # Loops through all the techniques used in the different projects
    # _counter keep track of how many projects that uses that specific technique
    # _names hold all the techniques and sort them in an ascending order
    for techs in retrieve_techniques()[1]:
        _counter = 0
        _names = []
        for rows in _data:
            if rows["techniques_used"].count(techs) > 0:
                _counter += 1
                _names.append({"id": rows["project_no"], "name": rows["project_name"]})
            _names = sorted(_names, key=lambda x: x["name"])
        _list.append({"count": _counter, "name": techs, "projects": _names})

    if len(_list) > 0:
        _error_code = 0
        _log.append("Called retrieve_techniques_stats() at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ".\n")
    else:
        _error_code = 1
        _log.append("Failed to call retrieve_techniques_stats() at " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ". Error-code: " + str(_error_code) + "\n")

    log()
    return (_error_code, _list)

# This is suppose to edit the CSV-file. It works to edit in _data but I can't figure out how to write it to the CSV file with the fieldnames. Don't need it for the project so I will not continue on this, for now.
'''
def edit_project(id,values):
    _error_code = 0
    init()
    if isinstance(values, dict):
        #Works but I think I need to edit in _data directly when looping it
#        u = [y for y in _data if y["project_no"] == id][0]
#        for i in values:
#            print i
#            print values[i]
        for i in _data:
            for o in values:
                if i["project_no"] == id:
                    if isinstance(values[o], str):
                        i[o] = unicode(values[o], "utf-8", errors="ignore")
                    else:
                        i[o] = values[o]
                    
                    if values["techniques_used"] and values["techniques_used"] != None:
                        i[o] = i["techniques_used"].split(",")
                    else:
                        i[o] = []

        # Write everything to the CSV-file
        fieldnames = csv.reader(open("data2.csv", "r")).next()
        csv_writer("data2.csv", _data, fieldnames)

    else:
        _error_code = 1
        error = "Values need to be in a dictionary."

    return (_error_code)

# Doesn't work with the fieldnames....
# DOES NOT WORK!!!!!!!!!!!!!!!
def csv_writer(csvfile22, values, fieldnames):
    f = open(csvfile22, "wb")
    writer = csv.DictWriter(f, fieldnames=fieldnames)
#    for i in values:
#        print i
#    writer = csv.writer(f)
    headers = {}
    for n in fieldnames:
        headers[n] = n
    writer.writerow(headers)
    for i in values:
        print i
        writer.writerows(i)
        for o in i:
            if isinstance(i[o], str):
                print o
#                print i[o].encode("utf-8")
#                writer.writerows(i[o].encode("utf-8"))
#            else:
#                print i[o]
#                writer.writerows(i[o])
#            print o.values().encode("utf-8", "ignore")
#        writer.writerow(i)
#    writer.writerow(values)
'''

def log():
    # This will open the LOG-file that is in the root-folder of the project and write the lines that are in _log and then empty _log

    global _log
    print _log
    try:
        f = open("../LOG", "a")
        f.writelines(_log)
        f.close()
        _log = []
    except IOError:
        return "Log-file doesn't exist."
