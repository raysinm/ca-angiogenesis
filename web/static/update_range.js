// Get all the range inputs
const rangeInputs = document.querySelectorAll('input[type="range"]');
const numberInputs = document.querySelectorAll('input[type="number"]');
const resetButtons = document.querySelectorAll('.reset-button');
const resetAllButton = document.getElementById('reset-all-button');
const defaultValues = {};

// Store the default values for each input
rangeInputs.forEach(input => {
  defaultValues[input.id] = input.value;
});

// Update range and number inputs on value change
function updateInputs(inputId, value) {
  const rangeInput = document.getElementById(inputId);
  const numberInput = document.querySelector(`input[type="number"][name="${inputId}"]`);
  
  rangeInput.value = value;
  numberInput.value = value;
}

// Update range input on range value change
rangeInputs.forEach(input => {
  const numberInput = document.querySelector(`input[type="number"][name="${input.id}"]`);

  input.addEventListener('input', () => {
    numberInput.value = input.value;
  });
});

// Update number input on number value change
numberInputs.forEach(input => {
  const rangeInput = document.getElementById(input.name);

  input.addEventListener('input', () => {
    rangeInput.value = input.value;
  });
});

// Reset individual input to default value
resetButtons.forEach(button => {
  const inputId = button.getAttribute('data-input-id');
  const defaultValue = defaultValues[inputId];

  button.addEventListener('click', () => {
    updateInputs(inputId, defaultValue);
  });
});

// Reset all inputs to default values
resetAllButton.addEventListener('click', () => {
  rangeInputs.forEach(input => {
    const defaultValue = defaultValues[input.id];
    updateInputs(input.id, defaultValue);
  });
});

// Submit form event handling
document.getElementById('run-simulation-form').addEventListener('submit', event => {
  event.preventDefault();
  // Your code for handling form submission
});
