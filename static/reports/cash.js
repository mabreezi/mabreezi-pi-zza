

var data = [
    { x: ['1', '2', '3', '4', '5'], y: [200000000, 185000000, 80000000, 30000000, 28000000 ],
        name: 'Cash Disbursed', type: 'bar'},

    { x: ['1', '2', '3', '4', '5'], y: [128000000, 185000000, 80000000, 28700000, 27500000],
        name: 'Cash Withdrawn', type: 'bar'}
];

var layout = {
    barmode : 'group',
    title : 'Cash Disbursed vs Cash Withdrawn: Last Seven days',
    autosize: false,
    // # width:650,
    // # height:450,
};


Plotly.newPlot('cash-disbursed', data, layout);


///////////////////////////


 var data = [
    {
        x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        y: [20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
        type: 'bar', name: 'Conditional Cash',
        'marker': {
            'color': 'rgb(49,130,189)',
            'opacity': 0.7,
        }
},

{
    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    y: [19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
    type: 'bar',
    name: 'Unconditional Cash',
    'marker': {
        'color': 'rgb(204,204,204)',
        'opacity': 0.5
    }
}

];

var layout = {
    title: 'Cash Spend 2017 (million)',
    'xaxis': {
        'tickangle': -45
    },
    barmode: 'group',
    autosize : false
};

Plotly.newPlot('cash-type-received', data, layout);

//////////////////////////////

 var data = [
    {
    x: ['2018-03-21','2018-03-22', '2018-03-23', '2018-03-24', '2018-03-25','2018-03-26', '2018-03-27'],
    y : [162748000, 68472000, 30870000, 55200000, 30320000, 41556000, 40654000],
    line : {'color' : '#17BECF'},
    type : "scatter",
    mode : "lines",
    name : 'Total',
},
    {
    x: ['2018-03-21','2018-03-22', '2018-03-23', '2018-03-24', '2018-03-25','2018-03-26', '2018-03-27'],
    y : [43540000, 24510000, 10430000, 5900000, 15450000,12500000, 4180000],
    line : {'color' : '#7F7F7F'},
    type : "scatter",
    mode : "lines",
    name : 'Zone 1',
},

];

var layout = {
    title: 'Cash Recieved by Zone',
    xaxis: {
        tickangle: -45
    },
    barmode: 'group',
    autosize : false
};

Plotly.newPlot('cash-by-zone', data, layout);