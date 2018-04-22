 
 
var data = [
    { x: ['Posho', 'Beans', 'Phones', 'Sanitary Pads', 'Seeds'], 
     y : [134523, 134523, 23042, 53689, 12585],
        type : 'bar'},
];

 var layout = {
    title : 'Refugees served by Item',
    autosize : false,
    // # width:650,
    // # height:450,
}

Plotly.newPlot('recipients-by-item', data, layout);


////////////////////

var data = [
    { x: [1,2,3,4,5], 
    y: [24569, 10345, 12314, 9243, 4956],
     type: 'bar', name:'Posho'},
    
    { x: [1,2,3,4,5], 
    y: [15478, 27930, 43022, 13784, 3789],
     type: 'bar', name:'Beans'},

    { x: [1,2,3,4,5], 
    y: [41905, 41905, 1345, 25021, 5034],
     type: 'bar', name:'Phones'},
    
    { x: [1,2,3,4,5], 
    y: [23564, 23564, 302, 13485, 756],
     type: 'bar', name:'Sanitary Pads'},
];
// # x: ['Posho', 'Beans', 'Phones', 'Sanitary Pads', 'Seeds'], 
// # y: [134523, 134523, 23042, 53689, 12585],

var layout = {
    title : 'Refugees served by Item',
    autosize: false,
    barmode: 'stack',
    xaxis:{
        title:'Zone'
    }
    // # width:650,
    // # height:450,
};

Plotly.newPlot('disbursements-by-zone', data, layout);


//////////////////

var data = [
    {
        x:['2017-09-30','2017-10-31', '2017-11-30', '2017-12-31', '2018-01-31', '2018-02-28', '2018-03-31'],
        y: [53563, 57969, 56345, 58453, 59345, 58345, 58854, 64567],
        type : "scatter",
        mode : "lines",
        name : 'Refugees',
    },

    {
        x:['2017-09-30','2017-10-31', '2017-11-30', '2017-12-31', '2018-01-31', '2018-02-28', '2018-03-31'],
        y:[1342, 1265, 1423, 1144, 1492, 1290, 1199, 1324],
        type : "scatter",
        mode : "lines",
        name : 'Host Community',
    }
];

var layout = {
    title : 'Beneficiaries of NCIs',
    xaxis: {
        range : ['2017-09-28', '2018-04-03'],
        type: 'date'
        },
    autosize : false        

};

Plotly.newPlot('beneficiaries-time-series', data, layout);