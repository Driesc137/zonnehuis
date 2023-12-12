const ctx2 = document.getElementById("lineChart2").getContext('2d');

// Voer een AJAX-verzoek uit om gegevens op te halen van de Python-server
fetch('/get-data') // Maak een nieuwe route in je Flask-applicatie om de gegevens op te halen
    .then(response => response.json())
    .then(data => {
        createChart2(data);
    })
    .catch(error => {
        console.error('Fout bij het ophalen van gegevens:', error);
    });

function createChart2(data) {
    const chart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i),
            datasets: [
                {
                    label: 'Groen',
                    data: data,
                    borderColor: 'rgba(0, 255, 0, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Blauw',
                    data: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
                    borderColor: 'rgba(0, 0, 255, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Rood',
                    data: [24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1],
                    borderColor: 'rgba(255, 0, 0, 1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
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
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        filter: function (item, chart) {
                            // Hier kun je de weergave van legendes aanpassen
                            return !item.text.includes('Uit te schakelen dataset');
                        }
                    }
                }
            }
        }
    });
}
