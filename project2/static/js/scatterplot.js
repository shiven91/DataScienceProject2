// $(document).ready(function () {
    
// });

var form = document.getElementById("myForm"); 
// function handleForm(event) { event.preventDefault(); } 
form.addEventListener('submit', myFunction);

function myFunction(event) {
    event.preventDefault()
    console.log("event --------------")
    console.log(event)

    const selectedMonth = document.getElementById('monthSelector');
    const selectedDay = document.getElementById('daySelector');
    const selectedYear = document.getElementById('yearSelector');

    
    const monthNum = selectedMonth.options[selectedMonth.selectedIndex].value
    const dayNum = selectedDay.options[selectedDay.selectedIndex].value
    const yearNum = selectedYear.options[selectedYear.selectedIndex].value
    console.log("month---------")
    console.log(monthNum)

    console.log("day---------")
    console.log(dayNum)
    console.log("year---------")
    console.log(yearNum)
    const parsedDate = Date.parse(`${monthNum}/${dayNum}/${yearNum}`)
    console.log(parsedDate)
    
}
    // Define the tooltip for hover-over info windows
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // Set the dimensions and margins of the graph
    var svg = d3.select("svg"),
        margin = { top: 20, right: 20, bottom: 60, left: 60 },
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom;
    // Set the ranges
    var x = d3.scaleTime().rangeRound([0, width]),
        y = d3.scaleLinear().rangeRound([height, 0]);
    // Append the SVG element with a g element
    // to offset the origin of the chart area by
    // the top-left margin
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    // USGS Real-Time Earthquake Feed
    //var usgs = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson";
    var usgs = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2017-06-02&endtime=2018-06-01&minmagnitude=5"
    // var formatTime = d3.timeFormat("%B %d, %Y");
    var formatTime = d3.timeFormat("%B %Y %I:%M %p");
    var time;
    var jsonData;
    var y;
    var x;
    // Create the scatterplot with the scatterplot data
    var scatterplot = "/geojson";
    d3.json(scatterplot, function (error, data) {
        if (error) console.log(error);
        console.log(data);
        jsonData = data;
        // Filter and format the data for use in the range
        //Y-Axis Properties
        magnitude = data.features.map(function (d) { return d.properties.mag; });
        //X-Axis Properties
        time = data.features.map(function (d) { return d.properties.time; });
        depth = data.features.map(function (d) { return d.geometry.coordinates[2]; });
        years = data.features.map(function (d) { return d.properties.place; });
        intensity = data.features.map(function (d) { return d.properties.place; });


        //t == time
        // var timeScale = []
        // for (var t=0; t < 500; t++) {
        //   timeScale[t] = time[t];
        // }
        // Scale the range of the data from the minimum value
        // to the maximum value
        // x.domain([d3.min(time)-1, d3.max(time)+1]);
        // y.domain([d3.min(magnitude)-1, d3.max(magnitude)+1]);
        x.domain([d3.min(time), d3.max(time)]);
        y.domain([d3.min(magnitude), d3.max(magnitude)]);

        // Add the X-Axis
        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            // .call(d3.axisBottom(x).ticks(20));
            .call(d3.axisBottom(x).tickFormat(formatTime));

        // Add a label for the X-Axis
        g.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.top + 20) + ")")
            .style("text-anchor", "middle")
            .style("font-size", "15px")
            .text("Time");

        // Add the Y-Axis
        g.append("g")
            .attr("class", "axis axis--y")
            .call(d3.axisLeft(y).ticks(10));

        // Add a label for the Y-Axis
        g.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", ".75em")
            .style("text-anchor", "middle")
            .style("font-size", "15px")
            .text("Magnitude");
        // Add the dots to the scatterplot with the tooltip
        g.selectAll(".dot")
            .data(data.features)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 10) //function (d) { return y(d.properties.mag) / 40; })
            .attr("cx", function (d) { return x(d.properties.time) })
            .attr("cy", function (d) { return y(d.properties.mag); })
            .on("mouseover", function (d) {
                console.log("----------------------------------")
                console.log("d    ----------------------------------")
                console.log(d)
                console.log(moment.utc(d.properties.time[0]).format("MM DD YYYY"))
                const eqTime = moment.utc(d.properties.time[0]).format("MM/DD/YYYY HH:MM:SS")
                console.log("----------------------------------")
                div.transition()
                    .duration(200)
                    .style("opacity", .9)
                    .style("stroke", "black");
                div.html("<div><b><u>Mag</b></u>: " + d.properties.mag
                    + "</div><br/>"
                    + "<div><u>Place</b></u >: " + d.properties.place
                    + "</div><br/>"
                    + "<div><u>Date</b></u >: " + eqTime
                    + "</div><br/>"


                    + "<div><b><u>Depth</b></u>: " + d.geometry.coordinates[2] + "km"
                    + "</div>")
                    .style("left", (d3.event.pageX + 10) + "px")
                    .style("top", (d3.event.pageY - 30) + "px");
            })
            .on("mouseout", function (d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
    });




