from flask import Flask, request, render_template
import json
from pathlib import Path
import sys

sys.path.append("../src/")
from vis import vis

base_path = Path(__file__).parent
config_path = (base_path / "../src/config.json").resolve()

app = Flask(__name__)


@app.route('/')
def index():
    if request.method == 'POST':
        update_config()
        # Call the vis function to generate the animation HTML
        animation_html = vis()
        # print(animation_html)
        return render_template('index.html', animation_html=animation_html)
    
    return render_template('index.html')
    
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
    }
    for form_key, form_value in form_data.items():
        for param, numerical_value in form_value.items():
            if numerical_value is not None and numerical_value is not '':
                config_data['defaults'][form_key][param] = float(numerical_value)
    
    # Write the updated data back to the file
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4)

    home = app.url_for(endpoint='index')
    return app.redirect(home)

if __name__ == '__main__':
    app.run(debug=True)
