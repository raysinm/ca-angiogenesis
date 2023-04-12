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
    
    if request.method == 'POST':
        update_config()

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
    parameters = {}
    
    with open(config_path, 'r') as f:
        config_data = json.load(f)

    form_data = {
    'tip_cell': {
    "p_migrate": request.form.get('tip_cell_p_migrate')
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
    for form_key, form_value in form_data.items():
        for param, numerical_value in form_value.items():
            if form_key in config_data['defaults'].keys() and numerical_value != None and numerical_value != '':
                config_data['defaults'][form_key][param] = float(numerical_value)
    
    form_data_generations = form_data['graphics']['generations'] #TODO: fix me
    if form_data_generations != None and form_data_generations != '':
        config_data['graphics']['generations'] = int(form_data_generations)    
    # Write the updated data back to the file
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4)

    home = app.url_for(endpoint='index')
    return app.redirect(home)

if __name__ == '__main__':
    app.run(debug=True)
