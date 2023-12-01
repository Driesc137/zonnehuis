document.getElementById('runPythonButton').addEventListener('click', function() {
    // Maak een HTTP-verzoek naar je Python-server om de code uit te voeren
    fetch('/Users/sennestans/TestPno/script.py')
        .then(response => response.text())
        .then(data => {
            // Toon de uitvoer op het dashboard
            document.getElementById('pythonOutput').textContent = data;
        })
        .catch(error => {
            console.error('Er is een fout opgetreden:', error);
        });
});
