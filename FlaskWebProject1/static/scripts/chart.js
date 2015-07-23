/**
 * Created by t846432 on 20.07.2015.
 */
$(function () {
    /*
    $.ajax({
        url: '/json/' + '{{title}}',
        //data: JSON.stringify({ 'id': '{{title}}' }),
        type: 'GET',
        beforeSend: function () {
            //$('#container').highcharts().showLoading();
        },
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            var ohlc = [];
            var volume = [];

            $.each(data.result, function (e, o) {
                ohlc.push(
                    [Date.parse(o[0]), o[1], o[2], o[3], o[4]]
                );

                volume.push(
                    [Date.parse(o[0]), o[5]]
                );
            });
            createchart(ohlc, volume);
            //$('#container').highcharts().hideLoading();
        }
    });
    */
    alert("test");
    // create the chart
    function createchart(ohlc, volume) {

        $('#container').highcharts('StockChart', {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: 'Stock Price'
            },
            events: {
                click: function (e) {
                    console.log(this), this
                },

            },
            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'OHLC'
                },
                height: '60%',
                lineWidth: 2
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Volume'
                },
                top: '65%',
                height: '35%',
                offset: 0,
                lineWidth: 2
            }],
            series: [{
                type: 'candlestick',
                name: 'Stock Price',
                data: ohlc,
                dataGrouping: {
                    units: [
                        [
                            'week', // unit name
                            [1] // allowed multiples
                        ], [
                            'month',
                            [1, 2, 3, 4, 6]
                        ]
                    ]
                }
            }, {
                type: 'column',
                name: 'Volume',
                data: volume,
                yAxis: 1,
                dataGrouping: {
                    units: [
                        [
                            'week', // unit name
                            [1] // allowed multiples
                        ], [
                            'month',
                            [1, 2, 3, 4, 6]
                        ]
                    ]
                }
            }]

        });

        var chart = $('#container').highcharts().annotations.allItems;
        console.log(chart);
    }
});
