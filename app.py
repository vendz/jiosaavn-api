from flask import Flask, jsonify, request
from flask_cors import CORS
import jiosaavn

app = Flask(__name__)
app.secret_key = 'xec97xb2x8fxd9xd8xed}&sxdbxc0x86Vx87&xa5xcb'
CORS(app)


@app.route('/')
def home():
    return "API is UP and running"


@app.route('/song')
def song():
    query = request.args.get('query')
    if query:
        return jsonify(jiosaavn.search_for_song(query))
    else:
        error = {
            'success': False,
            'message': 'You need to enter a query',
            'data': [],
        }
        return jsonify(error)


@app.route('/playlist')
def playlist():
    query = request.args.get('query')
    if query:
        return jsonify(jiosaavn.search_for_playlist(query))
        # try:
        #     val = int(query)
        #     return jsonify(jiosaavn.get_playlist(query))
        # except Exception:
        #     return jsonify(jiosaavn.search_for_playlist(query))
    else:
        error = {
            'success': False,
            'message': 'You need to enter a query',
            'data': [],
        }
        return jsonify(error)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
