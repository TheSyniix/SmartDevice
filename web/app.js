
class App{
    constructor(){
        this.getData().then(()=>{
            console.log(this.data);
            this.drawChart()
        })
        
    }
    
    async getData(){
        await fetch("http://localhost:3030/fetch").then(response =>{
            return response.json();
            }).then(data =>{
                this.data = data;
            });

    }

    drawChart(){
        const chart = document.getElementById('myChart');
        this.lineChart = new Chart(chart, {
                type:'line',
                data: {
                    labels:["this", "is", "a", "test"],
                    datasets: [
                        {
                            label:"Moisture Level (%)",
                            data:[this.data[0][1], this.data[1][1], this.data[2][1], this.data[3][1]]
                        }
                    ]
                }
            }
            );
    }
}

let app = new App();