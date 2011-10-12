#!/usr/bin/env python
# coding: utf-8

# imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response
import data

# Configuration
DEBUG = True
SECRET_KEY = "flaskrtdp003"
USERNAME = "tdp003"
PASSWORD = "tdp0033"

app = Flask(__name__)
app.config.from_object(__name__)

# Change to True when the site is live
#app.config.from_envvar('../FLASKR_SETTINGS', silent=False)

# Add a route for the /style-folder so flask know where to look for the css-file(s)
@app.route("/style/<filename>")
def css(filename): 
    with app.open_resource("style/" +filename) as f:
        return f.read()

# Same for the images as for the stylesheet(s)
@app.route("/images/<filename>")
def images(filename):
    with app.open_resource("images/" +filename) as f:
        return f.read()

@app.route("/")
def page_home():
    return render_template("home.html")

@app.route("/list", methods=["GET", "POST"])
def page_list():
    data.init()
    _highlight = None

    if request.method == "POST":

        _sort_by = "start_date"
        
        if request.form["sort_button"] == "Name":
            _sort_by = "project_name"
            _highlight = "name"
        elif request.form["sort_button"] == "ID":
            _sort_by = "project_no"
            _highlight = "id"
        elif request.form["sort_button"] == "Top projects":
            _sort_by = "lulz_had"
            _highlight = "top"

        _data = data.retrieve_projects(sort_by=_sort_by, search_fields=[_sort_by])[1]
    else:
        _data = data._data
        _highlight = None

    data_error = data._error_meaning[data._error_code]
    return render_template("list.html", _db_data=_data, _form_highlight = _highlight,data_error=data_error)

@app.route("/project/<id>")
def page_project(id):
    data.init()
    _project = data.lookup_project(id)[1]
    _error = data.lookup_project(id)[0]

    if _error > 0:
        _project = ""
#        _error = data._error_meaning[_error]

    data_error = data._error_meaning[data._error_code]
    return render_template("project.html", _db_data=_project, data_error=data_error)

@app.route("/techniques")
def page_techs():
    data.init()
    _techs = data.retrieve_technique_stats()[1]

    data_error = data._error_meaning[data._error_code]
    return render_template("techniques.html", _db_data=data._data, _techniques = _techs, data_error=data_error)

@app.route("/technique/<tech>")
def page_tech(tech):
    data.init()
    _techs = data.retrieve_technique_stats()[1]

    data_error = data._error_meaning[data._error_code]
    return render_template("technique.html", _db_data=data._data, _techniques = _techs,_tech=tech, data_error=data_error)

@app.route("/search", methods=["GET", "POST"])
def page_search():
    data.init()

    # keys is for the checkboxes
    keys = data._data[0].keys()
    techs = data.retrieve_techniques()[1]
    error = ""
    sstring = ""
    
    if request.method == "POST":
        _s_string = request.form["search_string"]
        _s_categories = request.form.getlist("search_categories")
        _s_sort_by = request.form["sort_category"]
        _s_sort_order = str(request.form["sort_order"])
        _s_techniques = request.form.getlist("search_techniques")

        if len(_s_categories) > 0:
            sstring = data.retrieve_projects(sort_by=_s_sort_by, sort_order=_s_sort_order, techniques=_s_techniques, search=_s_string, search_fields=_s_categories)[1]
        else:
            error = "You must specify at least one category to search in!"

    data_error = data._error_meaning[data._error_code]
    return render_template("search.html", _search_result = sstring, keys=keys, techs=techs, error=error, data_error=data_error)

@app.route("/admin")
def page_admin():
    data.init()

    data_error = data._error_meaning[data._error_code]
    return render_template("admin.html", data=data._data, data_error=data_error)

@app.route("/login", methods=["GET", "POST"])
def page_login():
    error = None

    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid Username."
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid Password."
        else:
            session["sess_admin"] = True
            flash("You were logged in.")
            return redirect(url_for("page_admin"))

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("sess_admin", None)
    flash("You were logged out.")
    return redirect(url_for("page_home"))

# This is for the editing of an entry in the CSV file. Won't work, read in data.py why.
#@app.route("/tools/apply", method=["GET", "POST"])
#def tools_apply(data):
#    data.init()
#    if data == "id":
#        return render_template("home.html")
'''
@app.route("/tools/<path:tool>", methods=["GET", "POST"])
def tools(tool):
    data.init()
    s_id = None
    keys = None
    te = None
    _data = data._data
    if tool == "edit":
        page = "edit.html"
    elif tool == "submit":
        page = "test.html"
    elif tool[0:7] == "edit_id":
        page = "edit_id.html"
        _data = data.lookup_project(tool[8:10])[1]
        s_id = tool[8:10]
        keys = data._data[0].keys()

        techs = data.retrieve_techniques()[1]
        te = ""
        for p in techs:
            te += p + ","

    elif tool[0:5] == "apply":
        
        page = "edit.html"

    # Don't need tool, just for dev
    return render_template("tools/" + page, data=_data,tool=tool,s_id=s_id,keys=keys,techs=te)
'''

if __name__ == "__main__":
    app.run(debug=False)
