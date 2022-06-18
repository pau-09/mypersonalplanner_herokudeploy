google.charts.load('current', {'packages':['corechart', 'bar']});

if(!total_count){
    removeChartsDivs();
}else{
    google.charts.setOnLoadCallback(drawSummaryChart);
    google.charts.setOnLoadCallback(drawAuthorsChart);
    google.charts.setOnLoadCallback(drawGenresChart);
}

function removeChartsDivs(){
    const main = document.querySelector('main');

    main.removeChild(document.querySelector('#summaryChart'));
    main.removeChild(document.querySelector('#vertical'));
    main.removeChild(document.querySelector('#authorsChart'));
    main.removeChild(document.querySelector('#horizontal'));
    main.removeChild(document.querySelector('#genresChart'));

    const warningDiv = document.createElement('div');
    warningDiv.setAttribute('id', 'noDataDiv');
    warningDiv.innerHTML = `<i><p>¡No tienes ninguna entrada!</p>
        <p>Agrega al menos una entrada a una de tus listas.</p></i>`;
    
    main.appendChild(warningDiv);
}

function drawSummaryChart() {
    const data = google.visualization.arrayToDataTable(statesData);

    const options = {
        backgroundColor: 'transparent',
        colors: ['#CBFFC1', '#FCEDC4', '#FCC4C4', '#C4D3FC'],
        fontName: 'Quicksand',
        is3D: true,
        legend:{
            alignment: 'center'
        },
        legendTextStyle: {
            color: '#8368A7',
            fontSize: 16,
        },
        pieSliceTextStyle: {
            color: '#9770A6',
        },
        title: 'Estados',
        titleTextStyle: {
            color: '#3B5DA0',
            fontSize: 20, 
            bold: true,
        },
    };

    const chart = new google.visualization.PieChart(document.getElementById('summaryChart'));

    chart.draw(data, options);
}

function drawAuthorsChart() {
    var data = google.visualization.arrayToDataTable(authorsData);

    const options = {
        backgroundColor: 'transparent',
        bars: 'horizontal',
        chartArea:{
            backgroundColor: 'transparent',
        },
        colors: ['#CBFFC1', '#FCEDC4', '#FCC4C4', '#C4D3FC'],
        fontName: 'Quicksand',
        hAxis: {
            baselineColor: '#8368A7',
            gridlines: {
                color: '#B476A7',
            },
            textStyle: {
                color: '#8368A7',
                fontName: 'Quicksand',
            },
        },
        legend:{
            position: 'none',
            alignment: 'center',
            textStyle: {
                color: '#8368A7',
                fontName: 'Quicksand',
                fontSize: 16,
            },
        },
        vAxis: {
            title:'',
            textStyle: {
                color: '#8368A7',
                fontName: 'Quicksand',
                bold: true,
            },
        },
        title: authorsDataTitle,
        titleTextStyle: {
            color: '#3B5DA0',
            fontSize: 20, 
            bold: true,
        },
    };

    const chart = new google.charts.Bar(document.querySelector('#authorsChart'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
}

function drawGenresChart() {
    const data = google.visualization.arrayToDataTable(genresData);

    const options = {
        backgroundColor: 'transparent',
        chartArea:{
            backgroundColor: 'transparent',
        },
        colors: ['#D88BA4'],
        fontName: 'Quicksand',
        hAxis: {
            textStyle: {
                color: '#8368A7',
                fontName: 'Quicksand',
                bold: true
            },
        },
        legend:{
            position: 'none'
        },
        vAxis: {
            baselineColor: '#8368A7',
            gridlines: {
                color: '#B476A7',
            },
            textStyle: {
                color: '#9770A6',
                fontName: 'Quicksand',
            },
        },
        title: 'Géneros',
        titleTextStyle: {
            color: '#3B5DA0',
            fontSize: 20, 
            bold: true,
        },
    };

    const chart = new google.visualization.ColumnChart(document.querySelector('#genresChart'));

    chart.draw(data, options);
}