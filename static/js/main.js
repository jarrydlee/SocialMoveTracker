// Main function
$(document).ready(function () {

  bindEvents();

});

// Bind events
var bindEvents = function () {
    getLineChartData();
    getSidebar();
};

var getLineChartData = function () {
    $.ajax({
        url: 'api/get_linechartdata',
        dataType: 'json',
        type: 'GET',
        success: function (data) {
            console.log(data);
            var date = new Date();
            var currentHour = date.getHours();
            labels: [currentHour]
            var chartData = {
                labels: ['' + currentHour-6 + ':00', '' + currentHour-5 + ':00', '' + currentHour-4 + ':00', ''
                            + currentHour-3 + ':00', '' + currentHour-2 + ':00', '' + currentHour-1 + ':00'
                        ],
                datasets: [
                    {
                        fillColor: "rgba(38,145,241,.4)",
                        strokeColor: "rgba(42,66,86,1)",
                        pointColor: "rgba(220,220,220,1)",
                        pointStrokeColor: "#fff",
                        data: [data[6], data[5], data[4], data[3], data[2], data[1]]
                    },
                    {
                        fillColor: "rgba(219,186,52,0.4)",
                        strokeColor: "rgba(246,59,87,1)",
                        pointColor: "rgba(220,220,220,1)",
                        pointStrokeColor: "#fff",
                        data: [20, 60, 42, 58, 31, 21, 50]
                    },
                ]
            };
            var options = {
                //Boolean - If we show the scale above the chart data
                scaleOverlay: false,
                //Boolean - If we want to override with a hard coded scale
                scaleOverride: true,
                //** Required if scaleOverride is true **
                //Number - The number of steps in a hard coded scale
                scaleSteps: 8,
                //Number - The value jump in the hard coded scale
                scaleStepWidth: 20,
                //Number - The scale starting value
                scaleStartValue: null,
                //String - Colour of the scale line
                scaleLineColor: "rgba(0,0,0,.1)",
                //Number - Pixel width of the scale line
                scaleLineWidth: 1,
                //Boolean - Whether to show labels on the scale
                scaleShowLabels: true,
                //Interpolated JS string - can access value
                scaleLabel: "<%=value%>",
                //String - Scale label font declaration for the scale label
                scaleFontFamily: "'Arial'",
                //Number - Scale label font size in pixels
                scaleFontSize: 12,
                //String - Scale label font weight style
                scaleFontStyle: "normal",
                //String - Scale label font colour
                scaleFontColor: "#666",
                ///Boolean - Whether grid lines are shown across the chart
                scaleShowGridLines: true,
                //String - Colour of the grid lines
                scaleGridLineColor: "rgba(0,0,0,.05)",
                //Number - Width of the grid lines
                scaleGridLineWidth: 1,
                //Boolean - Whether the line is curved between points
                bezierCurve: false,
                //Boolean - Whether to show a dot for each point
                pointDot: true,
                //Number - Radius of each point dot in pixels
                pointDotRadius: 3,
                //Number - Pixel width of point dot stroke
                pointDotStrokeWidth: 1,
                //Boolean - Whether to show a stroke for datasets
                datasetStroke: true,
                //Number - Pixel width of dataset stroke
                datasetStrokeWidth: 4,
                //Boolean - Whether to fill the dataset with a colour
                datasetFill: false,
                //Boolean - Whether to animate the chart
                animation: true,
                //Number - Number of animation steps
                animationSteps: 60,
                //String - Animation easing effect
                animationEasing: "easeOutQuart",
                //Function - Fires when the animation is complete
                onAnimationComplete: null
            };
            var ctx = $('#hourlyChart')[0].getContext("2d");
            new Chart(ctx).Line(chartData, options);
        }
    });
};

var getSidebar = function() {
    $.ajax({
        url: 'api/get_sidebar',
        dataType: 'json',
        type: 'GET',
        success: function (data) {
            console.log("getSidebar: " + data)
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var movie = key.toLowerCase().replace(/ /g, "").replace(/./g, "");
                    console.log(movie)
                    if (data[key] == 0) {
                        $('#movieSidebar').append('<li><a id=""+ movie +"" href="#">'+ key +'<span class=" text-success glyphicon glyphicon-circle-arrow-up pull-right"></span></a></li>')
                    } else if (data[key] == 1) {
                        $('#movieSidebar').append('<li><a id=""+ movie +"" href="#">'+ key +'<span class=" text-success glyphicon glyphicon-circle-arrow-up pull-right"></span></a></li>')
                    } else {
                        $('#movieSidebar').append('<li><a id=""+ movie +"" href="#">'+ key +'<span class=" text-danger glyphicon glyphicon-circle-arrow-down pull-right"></span></a></li>')
                    }
                }
            }
        }
    });

};

var processText = function (text) {
    var baseUrl = 'http://sentiment.vivekn.com/api/text/';


};


