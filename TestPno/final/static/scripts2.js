// SIDEBAR TOGGLE


function interpolateData(sourceData, targetLength) {
  const interpolatedData = Array.from({ length: targetLength }, (_, index) => {
    const sourceIndex = Math.floor((index / (targetLength - 1)) * (sourceData.length - 1));
    return sourceData[sourceIndex];
  });

  return interpolatedData;
}
// ---------- CHARTS ----------
fetch('/get-data') // Maak een nieuwe route in je Flask-applicatie om de gegevens op te halen
    .then(response => response.json())
    .then(data => {
        createCharts2(data);
        console.log(data[14])
        total = data[2] + data[3] + data[4] + 0;
    })
    .catch(error => {
        console.error('Fout bij het ophalen van gegevens:', error);
    });
// AREA CHART
function createCharts2(data, total) {
    const barChartOptions = {
      series: [
        {
          data: [data[2], data[4], data[3], 0],
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
      document.querySelector('#bar-chart2'),
      barChartOptions
    );
    barChart.render();
    
    // AREA CHART
    const areaChartOptions = {
      series: [
        
        {
          name: 'Buiten Temperatuur',
          data: data[9],
        },
      ],
      chart: {
        height: 350,
        type: 'area',
        toolbar: {
          show: false,
        },
      },
      colors: ['#cc3c43'],
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
            text: 'Temperatuur (°C)',
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
      document.querySelector('#area-chart2'),
      areaChartOptions
    );
    areaChart.render();
    // pie chart
    const options = {
      
      series: [data[2], data[4], data[3], 0],
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
    
    const chart = new ApexCharts(document.querySelector("#piechart2"), options);
    chart.render();
    
    const barChartOptions2 = {
        series: [
            {
              name: 'Wasmachine',
              data: data[6]
            },
            {
              name: 'Auto',
              data: data[5]
            },
            {
                name: 'Keuken',
                data: data[11]
              },
          ],
          chart: {
            height: 240,
            type: 'heatmap',
          },
          dataLabels: {
            enabled: false
          },
          colors: ["#008FFB"],
          title: {
            text: 'Wat verbruikt wanneer'
          },
          xaxis: {
            type: 'categories',
            categories: ['06','07','08','09','10','11','12','13','14','15','16', '17', '18', '19', '20', '21', '22', '23', '00','01','02','03','04','05'],
            labels: {
              show: true,
              rotate: -45,
              formatter: function (val) {
                return val;
              }
            }
          }
        };
      
      const barChart2 = new ApexCharts(
        document.querySelector('#bar2-chart2'),
        barChartOptions2
      );
      barChart2.render();
    
    
    
    
    // AREA CHART
    const areaChartOptions3 = {
        series: [
          {
            name: 'Verbruik Warmtepomp',
            data: data[7],
          },
          {
            name: 'Verbruik Airco',
            data: data[12],
          },
          
        ],
        chart: {
          height: 350,
          type: 'area',
          toolbar: {
            show: false,
          },
        },
        colors: ['#cc3c43','#246dec'],
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
        },
        labels: ['06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30', '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30'],
        markers: {
          size: 0,
        },
        yaxis: [
          {
            title: {
              text: 'Vermogen (Wh)',
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
      
      const areaChart3 = new ApexCharts(
        document.querySelector('#area-chart3'),
        areaChartOptions3
      );
      areaChart3.render();
 
    // AREA CHART
      
    const areaChartOptions7 = {
      series: [
        {
          name: 'Temperatuur per 15 seconden',
          data: data[14],
        },
        {
          name: 'Benaderde Temperatuur',
          data: interpolateData(data[8], data[14].length),
        },
      ],
      chart: {
        height: 350,
        type: 'area',
        toolbar: {
          show: false,
        },
      },
      colors: ['#7e4e9e', '#cc3c43'],
      dataLabels: {
        enabled: false,
      },
      stroke: {
        width: [1, 1, 1],
        curve: 'straight',
        dashArray: [0, 8, 5],
      },
      markers: {
        size: 0,
      },
      xaxis: {
        tickAmount: 24,
        overwriteCategories: [
          '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '00', '01', '02', '03', '04', '05'
        ],
      },
      yaxis: [
        {
          title: {
            text: 'Temperatuur (°C)',
          },
          labels: {
            formatter: function (val) {
              return val.toFixed(0);
            },
          },
          min: 15,  // Minimum waarde voor de y-as
          max: 26,  // Maximum waarde voor de y-as
        },
      ],
      tooltip: {
        shared: true,
        intersect: false,
        y: {
          formatter: function (val) {
            return val;
          },
        },
      },
    };
    
    const areaChart7 = new ApexCharts(
      document.querySelector('#chart7'),
      areaChartOptions7
    );
    areaChart7.render();
    

    
      
    
    const areaChartOptions9 = {
      series: [
        {
          name: 'Batterij Percentage',
          data: data[15],
        },
      ],
      chart: {
        height: 350,
        type: 'area',
        toolbar: {
          show: false,
        },
      },
      colors: ['#7e4e9e'],
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
            text: 'Batterij Percentage (%)',
          },
          labels: {
            formatter: function (val) {
              return val.toFixed(0); // Dit zorgt ervoor dat er geen decimalen worden weergegeven
            },
          },
          min: 0, // Stel het minimum van de y-as in op 0
          max: 100, // Stel het maximum van de y-as in op 100
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
    
    const areaChart9 = new ApexCharts(
      document.querySelector('#area-chart9'),
      areaChartOptions9
    );
    areaChart9.render();

    const areaChartOptions10 = {
      series: [
        {
          name: 'Irradiantie',
          data: data[16],
        },
      ],
      chart: {
        height: 350,
        type: 'area',
        toolbar: {
          show: false,
        },
      },
      colors: ['#000080',],
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
            text: 'Irradiantie (W/m²)',
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
    
    const areaChart10 = new ApexCharts(
      document.querySelector('#area-chart10'),
      areaChartOptions10
    );
    areaChart10.render();



    const areaChartOptions11 = {
      series: [
        {
          name: 'Elektriciteitsprijs',
          data: data[17],
        },
      ],
      chart: {
        height: 350,
        type: 'area',
        toolbar: {
          show: false,
        },
      },
      colors: ['#f5b74f'],
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
            text: 'Elektriciteitsprijs (€/MWh)',
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
    
    const areaChart11 = new ApexCharts(
      document.querySelector('#area-chart11'),
      areaChartOptions11
    );
    areaChart11.render();
    }
    
