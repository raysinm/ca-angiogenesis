from flask import Flask, request, render_template, jsonify
import json
from pathlib import Path
import sys
sys.path.append("../src/")

import engine_client

base_path = Path(__file__).parent
config_path = (base_path / "../src/config.json").resolve()
#TODO: add src_path = ... .resolve()
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
    
# @app.route('/matrix_list')
# def response_matrix_list():
#     # check if request is made via AJAX
#     #if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#     matrix_list = vis()
#     return jsonify(matrix_list)

@app.route('/run_simulation', methods=['POST'])
def run_simulation():

    animation_gif = engine_client.run(request.form)

    # Should call the server with the form dict from the html  
    # home = app.url_for(endpoint='index')
    # return app.redirect(home)
    return animation_gif    #Danger: whats being passed?

if __name__ == '__main__':
    app.run(debug=True)
