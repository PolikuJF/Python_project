from flask import Flask, render_template, request
from Python_project2.Minecraft_parser import update_date, get_serverss

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    sort_by = request.args.get('sort_by', '')
    search = request.args.get('search', '')
    order = request.args.get('order', 'asc')
    if (request.args.get('update', '') == '1') :
        serverss = update_date()
    serverss = get_serverss(sort_by, order, search)
    return render_template("index.html", serverss=serverss, current_order=order, current_search=search, current_sort=sort_by)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)