from flask import Flask, request, render_template, jsonify
import json
from pathlib import Path
import sys
sys.path.append("../src/")
from vis import vis

base_path = Path(__file__).parent
config_path = (base_path / "../src/config.json").resolve()
#TODO: add src_path = ... .resolve()
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    
    # if request.method == 'POST':
    #     update_config()

    return render_template('index.html')
    
@app.route('/matrix_list')
def response_matrix_list():
    # check if request is made via AJAX
    #if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    matrix_list = vis()
    return jsonify(matrix_list)
    return

@app.route('/update_config', methods=['POST'])
def update_config():
    # Should call the server with the form dict from the html  
    home = app.url_for(endpoint='index')
    return app.redirect(home)

if __name__ == '__main__':
    app.run(debug=True)
