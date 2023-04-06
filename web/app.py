from flask import Flask, request, render_template
import json

app = Flask(__name__)

# This is just an example dictionary of parameters
# parameters = {"param1": 0, "param2": 0}

@app.route('/')
def index():
    # Render the HTML form
    return render_template('index.html')

@app.route('/update_config', methods=['POST'])
def update_config():
    # Get the parameters from the request form
    
    parameters = {}
    # Get the parameters from the request form
    # parameters = request.form.to_dict(flat=False)
    # parameters = json.loads(parameters_json)
    # Read in the existing config data
    with open('../src/config.json', 'r') as f:
        config_data = json.load(f)

    print(config_data)

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
    with open('../src/config.json', 'w') as f:
        json.dump(config_data, f, indent=4)

    home = app.url_for(endpoint='index')
    return app.redirect(home)


if __name__ == '__main__':
    app.run(debug=True)
