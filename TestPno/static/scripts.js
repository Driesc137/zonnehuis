// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------
fetch('/get-data') // Maak een nieuwe route in je Flask-applicatie om de gegevens op te halen
    .then(response => response.json())
    .then(data => {
        createCharts(data);
    })
    .catch(error => {
        console.error('Fout bij het ophalen van gegevens:', error);
    });
// BAR CHART
function createCharts(data) {
const barChartOptions = {
  series: [
    {
      data: [10, 8, 6, 4],
    },
  ],
  chart: {
    type: 'bar',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f'],
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
    categories: ['Wasmachine', 'Verwarming', 'Auto', 'Keuken'],
  },
  yaxis: {
    title: {
      text: 'Verbruik',
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
      data: data,
    },
    {
      name: 'Verbruikte energie',
      data: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
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
  labels: ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16', '17', '18', '19', '20', '21', '22', '23'],
  markers: {
    size: 0,
  },
  yaxis: [
    {
      title: {
        text: 'Energie',
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
  },
};

const areaChart = new ApexCharts(
  document.querySelector('#area-chart'),
  areaChartOptions
);
areaChart.render();
// pie chart
const options = {
  series: [44, 55, 13, 43],
  chart: {
  width: 380,
  type: 'pie',
},
colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f'],
labels: ['Wasmachine', 'Verwarming', 'Auto', 'Keuken'],
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