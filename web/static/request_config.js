// Load the config.json file using an HTTP request
const request = new XMLHttpRequest();
request.open('GET', '../../src/config.json');
request.responseType = 'json';
request.send();
request.onload = function() {
    const config = request.response;

    // Update the slider and text box values when the page loads
    updateValues('tip_cell', 'p_migrate', config.defaults.tip_cell.p_migrate);
    updateValues('attractor_cell', 'attraction_generated', config.defaults.attractor_cell.attraction_generated);
    updateValues('stalk_cell', 'p_sprout', config.defaults.stalk_cell.p_sprout);
}
