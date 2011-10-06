#!/usr/bin/env python
# coding: utf-8

# imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response
import data

app = Flask(__name__)

app.static_folder = "style"
app.add_url_rule("/style/<path:filename>", endpoint="static", view_func=app.send_static_file)

app.add_url_rule("/images/<path:filename>", endpoint="images", view_func=app.send_static_file)

@app.route("/style/<filename>")
def css(filename): pass

@app.route("/images/<filename>")
def images(filename): pass

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

    return render_template("list.html", _db_data=_data, _form_highlight = _highlight)

@app.route("/project/<id>")
def page_project(id):
    data.init()
    return render_template("project.html", _db_data=data._data, _show_id=int(id))

if __name__ == "__main__":
    app.run(debug=True)
