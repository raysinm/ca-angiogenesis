function initParameters() {
    return {
        "tip_cell": {
            "p_migrate": 0.9
        },
        "attractor_cell": {
            "attraction_generated": 1e18
        },
        "stalk_cell": {
            "p_sprout": 0.008
        },
        "attraction": {
            "decay_coef": 0.7,
            "update_precision": 0.001
        }
    };
}

var parameters = initParameters();