const ctx = document.getElementById("lineChart1").getContext('2d');

// Voer een AJAX-verzoek uit om gegevens op te halen van de Python-server
fetch('/get-data') // Maak een nieuwe route in je Flask-applicatie om de gegevens op te halen
    .then(response => response.json())
    .then(data => {
        createChart1(data);
    })
    .catch(error => {
        console.error('Fout bij het ophalen van gegevens:', error);
    });

function createChart1(data) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i),
            datasets: [{
                label: 'Gegevens',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Uur'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Waarde'
                    }
                }
            }
        }
    });
}
