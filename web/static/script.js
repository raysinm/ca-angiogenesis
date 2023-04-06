const greetEvent = document.getElementById('greet');
const nameInput = document.getElementById('name');
const resultOutput = document.getElementById('result');

greetEvent.addEventListener('click', function() {
  //preventDefault();
  const name = nameInput.value;
  resultOutput.innerHTML = `Hello, ${name}!`;
});

nameInput.addEventListener('keyup', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    const name = nameInput.value;
    resultOutput.innerHTML = `Hello, ${name}!`;
  }
});
