
var data = [
    {
        values : [811481, 492442, 32975],
        labels : ['Children (0-18)', 'Adults (18-59)', 'Adults (60+)'],
        type : 'pie'
    }
];

var layout = {
    title : 'Zonal Statistical Summary',
    autosize: false
};

Plotly.newPlot('age-makeup', data, layout);


//////////////////

var data = [
    {
        values : [940843, 41882, 180000],
        labels : ['Refugees', 'Asylum Seekers', 'People of Concern'],
        type : 'pie'
    }
];

var layout = {
    title : 'Makeup of the Recipients',
    autosize : false
};

Plotly.newPlot('recipient-makeup', data, layout);