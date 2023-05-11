from flask import Flask, request, render_template, jsonify
import json
# from pathlib import Path
import sys
sys.path.append("../web/")

from . import engine_client

# base_path = Path(__file__).parent
# config_path = (base_path / "../src/config.json").resolve()
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

    form_data = {
        'tip_cell': {
        "p_migrate": request.form.get('tip_cell_p_migrate')       #! Does 'get' work like this? 
        },
        'attractor_cell' : {
            "attraction_generated": request.form.get('attractor_cell_attraction_generated')
        },
        'stalk_cell' : {
            "p_sprout": request.form.get('stalk_cell_p_sprout')
        },
        'attraction' : {
            "decay_coef": request.form.get('attraction_decay_coef'),
            "update_precision": request.form.get('attraction_update_precision')
        },
        'graphics': {
            'generations' : request.form.get('graphics_generations')
        } 
        }

    # Sending params and getting animation over gRPC
    animation_gif = engine_client.run(json.dumps(form_data))

    # Should call the server with the form dict from the html  
    # home = app.url_for(endpoint='index')
    # return app.redirect(home)
    return json.dumps(animation_gif)    #Danger: whats being passed?    --currently, a string with a dictionary of 'animation' and 'type'

if __name__ == '__main__':
    app.run(debug=True)
