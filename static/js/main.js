google.charts.load('current', {'packages':['corechart', 'bar']});

if(!book_count && !movie_count){
    removeChartsDivs();
}else{
    google.charts.setOnLoadCallback(drawStatesChart);
    google.charts.setOnLoadCallback(drawTotalCountChart);
}

function removeChartsDivs(){
    const main = document.querySelector('main');

    main.removeChild(document.querySelector('#totalCountChart'));
    main.removeChild(document.querySelector('hr'));
    main.removeChild(document.querySelector('#statesChart'));

    const warningDiv = document.createElement('div');
    warningDiv.setAttribute('id', 'noDataDiv');
    warningDiv.innerHTML = `<i><p>¡No tienes ninguna entrada!</p>
        <p>Agrega al menos un libro o una película a una de tus listas.</p></i>`;
    
    main.appendChild(warningDiv);

}

function drawStatesChart() {
    var data = google.visualization.arrayToDataTable(summaryData);
    
    var options = {
        animation:{
            duration: 500,
            startup: true,
        },
        backgroundColor: 'transparent',
        colors: ["#F0A6A5", "#4570C3"],
        fontName: 'Quicksand',
        hAxis: {
            textStyle: {
                color: '#8368A7',
                fontSize: 18, 
                bold: true,
            },
        },
        legend:{
            position: 'bottom',
            alignment: 'center',
            textStyle: {
                color: '#8368A7',
                fontSize: 18,
            },
        },
        vAxis: {
            title:'',
            baselineColor: '#8368A7',
            textStyle: {
                color: '#8368A7',
                fontSize: 16, 
                bold: true,
            },
            gridlines: {
                color: '#B19ECA',
                multiple: 1
            },
            minorGridlines: {
                count: 0
            },
        },
    
    };

    var chart = new google.visualization.ColumnChart(document.querySelector('#statesChart'));
    chart.draw(data, options);
}

function drawTotalCountChart() {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Tipo')
    data.addColumn('number', 'Total')
    data.addRows([
        ['Libros', book_count],
        ['Películas', movie_count],
    ])

    const options = {
        backgroundColor: 'transparent',
        colors: ["#F0A6A5", "#4570C3"],
        fontName: 'Quicksand',
        is3D: true,
        legend:{
            alignment: 'center',
            position: 'bottom',
        },
        legendTextStyle: {
            color: '#8368A7',
            fontSize: 18,
        },
        pieSliceTextStyle: {
            color: '#201824',
        },
    };

    const chart = new google.visualization.PieChart(document.querySelector('#totalCountChart'));
    chart.draw(data, options);
}