// SIDEBAR TOGGLE
/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
} 


$(document).ready(function () {
  $("#sidebarCollapse").on("click", function () {
    $("#sidebar").toggleClass("active");
  });
});

// ---------- CHARTS ----------
fetch('/get-data') // Maak een nieuwe route in je Flask-applicatie om de gegevens op te halen
    .then(response => response.json())
    .then(data => {
        createCharts(data);
        total = data[2] + data[3] + data[4] + 0;
    })
    .catch(error => {
        console.error('Fout bij het ophalen van gegevens:', error);
    });
// BAR CHART
function createCharts(data, total) {
const barChartOptions = {
  series: [
    {
      data: [data[2], data[4],data[13], data[3], data[10]],
    },
  ],
  chart: {
    type: 'bar',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f','#7e4e9e'],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: false,
      columnWidth: '40%',
    },
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },
  xaxis: {
    categories: ['Wasmachine', 'Verwarming','Airco', 'Auto', 'Keuken'],
  },
  yaxis: {
    title: {
      text: 'Verbruik (kWh)',
    },
    labels: {
      formatter: function (val) {
        return val.toFixed(0); // Dit zorgt ervoor dat er geen decimalen worden weergegeven
      },
    },
  },
};

const barChart = new ApexCharts(
  document.querySelector('#bar-chart'),
  barChartOptions
);
barChart.render();

// AREA CHART
const areaChartOptions = {
  series: [
    {
      name: 'Opgewekte energie',
      data: data[0],
    },
    {
      name: 'Verbruikte energie',
      data: data[1],
    },
  ],
  chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false,
    },
  },
  colors: ['#367952', '#cc3c43'],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
  },
  labels: ['06','07','08','09','10','11','12','13','14','15','16', '17', '18', '19', '20', '21', '22', '23', '00','01','02','03','04','05'],
  markers: {
    size: 0,
  },
  yaxis: [
    {
      title: {
        text: 'Energie (kWh)',
      },
      labels: {
        formatter: function (val) {
          return val.toFixed(0); // Dit zorgt ervoor dat er geen decimalen worden weergegeven
        },
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (val) {
        return val; // Gebruik de werkelijke waarde zonder afronding voor de tooltip
      },
    },
  },
};

const areaChart = new ApexCharts(
  document.querySelector('#area-chart'),
  areaChartOptions
);
areaChart.render();
// pie chart
const options = {
  
  series: [data[2], data[4],data[13], data[3], data[10]],
  chart: {
  width: 380,
  type: 'pie',
},
colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f','#7e4e9e'],
labels: ['Wasmachine', 'Verwarming','Airco', 'Auto', 'Keuken'],
responsive: [{
  breakpoint: 480,
  options: {
    chart: {
      width: 200
    },
    legend: {
      position: 'bottom'
    }
  }
}]
};

const chart = new ApexCharts(document.querySelector("#piechart"), options);
chart.render();
}