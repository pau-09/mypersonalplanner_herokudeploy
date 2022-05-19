google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawBookChart);
google.charts.setOnLoadCallback(drawMovieChart);

function drawBookChart() {
    var data = google.visualization.arrayToDataTable(books);

    var options = {
        title: 'Libros',
        titleTextStyle: {
            color: '#8368A7',
            fontName: 'quicksand',
            fontSize: 20, 
            bold: true,
        },
        backgroundColor: 'transparent',
        is3D: true,
        legend:{
            alignment: 'center'
        },
        legendTextStyle: {
            color: '#8368A7',
            fontName: 'quicksand',
            fontSize: 20,
        },
        pieSliceTextStyle: {
            color: '#9770A6',
        },
        colors: ['#CBFFC1', '#FCEDC4', '#FCC4C4', '#C4D3FC']
    };

    var chart = new google.visualization.PieChart(document.getElementById('bookChart'));

    chart.draw(data, options);
}

function drawMovieChart() {

    var data = google.visualization.arrayToDataTable(movies);

    var options = {
        title: 'Películas',
        titleTextStyle: {
            color: '#8368A7',
            fontName: 'quicksand',
            fontSize: 20, 
            bold: true,
        },
        backgroundColor: 'transparent',
        is3D: true,
        legend:{
            alignment: 'center'
        },
        legendTextStyle: {
            color: '#8368A7',
            fontName: 'quicksand',
            fontSize: 20,
        },
        pieSliceTextStyle: {
            color: '#9770A6',
        },
        colors: ['#CBFFC1', '#FCEDC4', '#FCC4C4', '#C4D3FC']
    };

    var chart = new google.visualization.PieChart(document.getElementById('movieChart'));

    chart.draw(data, options);
}