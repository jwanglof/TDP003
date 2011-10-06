from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response
import csv

#_csv_fieldnames = ("id","project_name","start_date","end_date","course_code","course_name","course_cred","techniques","summary","description","snapshot","group_size","link")

app = Flask(__name__)

app.static_folder = "style"
app.add_url_rule("/style/<path:filename>", endpoint="static", view_func=app.send_static_file)

#url_for("csvdata", filename="data.cvs")

@app.route("/data.cvs")
def show_data():
    def generate():
        for row in iter_all_rows():
            yield ",".join(row) + "\n"
    return Response(generate(), direct_passthrough=True, mimetype="text/csv")

@app.route("/style/<filename>")
def css(filename): pass

@app.route("/")
def root():
    return render_template("root.html")

@app.route("/list", methods=["GET", "POST"])
def list():
    _csv_data_file = open("data.csv", "rb")
    _csv_fieldnames = csv.reader(_csv_data_file).next()
    _csv_data = csv.DictReader(_csv_data_file, fieldnames=_csv_fieldnames)

    if request.method == "POST":
        _new_list = []

        if request.form["id"]:
            for rows in _csv_data:
                _new_list.append(rows["id"])

        elif request.form["name"]:
            for rows in _csv_data:
                _new_list.append(rows["project_name"])

        elif request.form["top"]:
            for rows in _csv_data:
                _new_list.append(rows["id"])
        
        _new_list.sort()

        _csv_data_file = open("data.csv", "rb")
        _csv_fieldnames = csv.reader(_csv_data_file).next()
        _csv_data = csv.DictReader(_csv_data_file, fieldnames=_csv_fieldnames)

        return render_template("list_sorted.html", data=_csv_data, _list=_new_list)
    
    else:
        #    _csv_data = csv.reader(open("data.csv", "r"), delimiter=",")
    #    data = [row for row in _csv_data]
        return render_template("list.html", data=_csv_data)

#@app.route("/projects")
#def projects():
#    return render_template("projects.html")

@app.route("/project/<id>")
def project(id):
    _csv_data_file = open("data.csv", "rb")
    _csv_fieldnames = csv.reader(_csv_data_file).next()
    _csv_data = csv.DictReader(_csv_data_file, fieldnames=_csv_fieldnames)
    return render_template("project.html", data=_csv_data, _show_id=id)

@app.route("/techniques")
def techniques():
    return render_template("techniques.html")

@app.route("/search", methods=["GET", "POST"])
def search():
#    _csv_data_file = open("data.csv", "rb")
    if request.method == "POST":
        with open("data.csv", "rb") as f:
            _csv_string = csv.reader(f)
#    _csv_data = csv.DictReader(_csv_data_file, fieldnames=_csv_fieldnames)
            if request.form["search_string"] in _csv_string:
                bla = "sadsad"
            else:
                bla = _csv_string
            return render_template("search.html", search_result=bla)

@app.route("/asd")
def asd():
    _csv_data_file = open("data.csv", "rb")
    _csv_fieldnames = csv.reader(_csv_data_file).next()
    _csv_data = csv.DictReader(_csv_data_file, fieldnames=_csv_fieldnames)
    return render_template("asd.html", data=_csv_data)

if not app.debug:
    import logging

if __name__ == "__main__":
    app.run(debug=True)
