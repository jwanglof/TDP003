#! /usr/bin/env python
# coding: utf-8
import csv, os

_error_code = 1
_data = []

f = open("data.csv", "r")
f_fieldnames = csv.reader(f).next()

# FAAAAAAAAAAAAAAAAAAAAAAAAAAAAIL!!!!    
def init():
    global _error_code
    global _data
    _data = []

    try:
        _csv_reader = csv.reader(open("data.csv", "r"))
        _csv_fieldnames = _csv_reader.next()
#        print _csv_fieldnames
#        print _csv_reader
        for row in _csv_reader:
            field = {}
#            print row
            for fieldName in _csv_fieldnames:
                # fieldName = The fieldnames
                # 
                index = _csv_fieldnames.index(fieldName)
                
                if not row[index].isdigit():
                    if len(row[index]) == 0:
                        field[fieldName] = None
                    else:
                        field[fieldName] = unicode(row[index], "utf-8")
#                        print field[fieldName]
                else:
                    if len(row[index]) > 1:
                        field[fieldName] = str(row[index])
                    else:
                        field[fieldName] = int(row[index])
            _data.append(field)
        
        for row in _data:
            if row["techniques_used"] != None:
                row["techniques_used"] = row["techniques_used"].split(",")
                row["techniques_used"].sort()
            else:
                row["techniques_used"] = []

        _error_code = 0
    except IOError:
        _error_code = 1

def project_count():
    global _error_code


    if _error_code != 1:
        _error_code = 0
#    print _error_code

    return (_error_code, len(_data))

def lookup_project(id):
    global _error_code
    global _data

    _proj = {}
    for i in _data:
        if int(i["project_no"]) == int(id):
            _proj = i
            
    if len(_proj) == 0:
        _error_code = 2
        _proj = None

    return (_error_code, _proj)

def retrieve_projects(sort_by="start_date",sort_order="asc",techniques=[],search="",search_fields=[]):
    # For testing
#    init()

#går igenom alla projekt i en loop
#i den loopen går man igenom alla techniques som man skickat in
#kolla om techniques finns i projektets tech-lista
#om det inte finns så ska inte projektet finnas med i resultatet

    global _error_code
    global _data
    global f_fieldnames
    _dict = {}
    _list = []

    if isinstance(techniques, list) and len(techniques) > 0:
        _techs = techniques
    else:
        _techs = None

    if isinstance(search_fields, list) and len(search_fields) > 0:
#        index_of_fieldname = f_fieldnames.index(_fields[0])
        _fields = search_fields
    else:
        _fields = None

    if isinstance(search, str) and len(search) > 0:
#        search = unicode(search, "utf-8").lower()
        search = unicode(search, "utf-8")
    else:
        search = None
    
    if _techs != None:
        for rows in _data:
            for tech in _techs:
                # funkar inte med >1 tekniker
                if tech in rows["techniques_used"] and len(rows["techniques_used"]) > 0:
                    _list.append(rows)
    else:
        _list = _data[:]

    #funkar inte om det er lowercase
    _new_list = []
#    print _list
    if search != None:
        if _fields != None:
            for field in _fields:
                for row in _list:
                    r_string = row[field]
                    
                    if type(r_string) is not unicode:
                        r_string = unicode(str(r_string), "utf-8")

#                    if type(r_string) is int:
#                        r_string = str(r_string)

                    if search.lower() in r_string.lower():
                        _new_list.append(row)
        else:
            _error_code = 0
#            for l_rows in _list:
#                if search in l_rows.values():
#                    _new_list.append(l_rows)
    else:
        _new_list = _list
#    print techniques
    if isinstance(sort_order, str) and len(sort_order) > 0:
        if sort_order == "desc":
            _new_list = sorted(_new_list, key=lambda project: project[sort_by],reverse=True)
        else:
            _new_list = sorted(_new_list, key=lambda project: project[sort_by])


    if _techs is None and _fields is None and search is None:
        _new_list = _data
    return (_error_code, _new_list)

def retrieve_techniques():
    # for testing
#    init()

    global _data
    global _error_code

    _list = []
    for rows in _data:
        _list.extend(rows["techniques_used"])
        
    _new_list = []
    for items in _list:
        if items not in _new_list:
            _new_list.append(items)

    _error_code = 0
    return (_error_code, sorted(_new_list))


def retrieve_technique_stats():
    #for testing
#    init()

    global _error_code
    global _data

    #to get all the techniques
    _unique_techs = retrieve_techniques()[1]

    _dict = {}
    _list = []
    for techs in _unique_techs:
        _counter = 0
        _names = []
        for rows in _data:
            if rows["techniques_used"].count(techs) > 0:
                _counter += 1
                _names.append({"id": rows["project_no"], "name": rows["project_name"]})
            _names = sorted(_names, key=lambda x: x["name"])
            _dict["projects"] = _names
            _dict["name"] = techs
            _dict["count"] = _counter
        _list.append({"count": _counter, "name": techs, "projects": _names})
    _error_code = 0
    return (_error_code, _list)
