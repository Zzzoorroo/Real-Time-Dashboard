Ploty.newPlot('ploty-chart', [{
    x: [],
    y: [],
    mode: 'lines+markers',
    type: 'scatter'
}], {
    title: 'Real-time Data',
    xaxis: {
        title: 'Time',
        automargin: true
    },
    yaxis: {
        title: 'Value',
    }
});
socket.on('updateValue', function (data) {
    console.log("Received updateValue:", data);
    times.push(data.time);
    values.push(data.value);
    if (times.length > 20) {
        times.shift();
        values.shift();
    }
    Ploty.update('ploty-chart', {x: [times], y: [values] });
});