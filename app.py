from flask import Flask, request, jsonify
from tinydb import TinyDB

from config import Config
from utils import find_form_for_request

app = Flask(__name__)
db = TinyDB(Config.DB)


@app.route('/get_form', methods=["POST"])
def get_form():
    data = request.form.to_dict()
    return jsonify(find_form_for_request(data, db))


if __name__ == '__main__':
    app.run()
