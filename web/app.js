const chart = document.getElementById('myChart');
let lineChart = new Chart(chart, {
        type:'line',
        data: {
            labels:["this", "is", "a", "test"],
            datasets: [
                {
                    label:"My first dataset",
                    data:[1, 2, 3, 4]
                }
            ]
        }
    }
    );