function ChartController($scope, $routeParams ) {
    $scope.ticker = $routeParams.ticker;
    $scope.loading = true;

    $scope.getchartdata = function(){
        //console.log($scope.chartConfig);
        //$scope.chartConfig.series[0].data.unshift([1426118400,10, 15, 8, 9]);
        //$scope.chartConfig.loading = true;
        $scope.loading = true;
        $.ajax({
            url: '/json/'+$scope.ticker,
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
                    //console.log(Date.parse(o[0]));
                    $scope.chartConfig.series[0].data.push(
                        [Date.parse(o[0]), o[1], o[2], o[3], o[4]]

                    );
                    $scope.chartConfig.series[0].id = $scope.ticker;
                    $scope.chartConfig.series[0].name = $scope.ticker;

                    volume.push(
                        [Date.parse(o[0]), o[5]]
                    );
                });

                //$scope.chartConfig.series.push({
                //    data: ohlc
                //})

                //$scope.data.push(ohlc);
                $scope.$apply();
                //$('#container').highcharts().hideLoading();
                $scope.loading = false;

            }
        });
    };
    $scope.toggleLoading = function () {
        this.chartConfig.loading = !this.chartConfig.loading
    }

    $scope.chartConfig = {
        options: {
            subtitle: {
                text: $scope.ticker
            },
            chart: {
                backgroundColor: 'transparent',
                //zoomType: 'xy',
                events: {
                    selection: function (e) {
                                $scope.status("Drag!"+ e.xAxis[0].min + " to " +e.xAxis[0].max);
                                $scope.$apply();
                            }
                    /*
                            click: function (e) {
                                $scope.newAnnotation(e);
                            }
*/
                        },
                resetZoomButton: {
                    position: {
                        x: 0,
                        y: -35
                    },
                    theme: {
                        fill: 'white',
                        stroke: 'silver',
                        r: 0,
                        states: {
                            hover: {
                                fill: '#41739D',
                                style: {
                                    color: 'white'
                                }
                            }
                        }
                    }
                }
            },
            navigator: {
                enabled: true,
                series: {
                    data: []
                }
            },
            rangeSelector: {
                enabled: false
            },
            plotOptions: {
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            /*
                            click: function () {
                                alert(this);
                            }
                            */
                        }
                    },
                    lineWidth: 1,
                    fillOpacity: 0.5

                },
                column: {
                    stacking: 'normal'
                },
                area: {
                    stacking: 'normal',
                    marker: {
                        enabled: false
                    }
                }

            },
            exporting: false,
            xAxis: [{
                type: 'datetime',
            }],
            yAxis: [

                { // Primary yAxis

                    min: 0,
                    allowDecimals: false,
                    title: {
                        //text: 'number of notification',
                        style: {
                            color: '#80a3ca'
                        }
                    },
                    labels: {
                        format: '{value}',
                        style: {
                            color: '#80a3ca'
                        }
                    }


                },
                { // Secondary yAxis
                    min: 0,
                    allowDecimals: false,
                    title: {
                        //text: 'price',
                        style: {
                            color: '#c680ca'
                        }
                    },
                    labels: {
                        format: '{value}',
                        style: {
                            color: '#c680ca'
                        }
                    },
                    opposite: true

                }
            ],

            legend: {
                enabled: false
            },
            title: {
                text: ' '
            },
            credits: {
                enabled: false
            },

            loading: $scope.loading,
            /*
            tooltip: {
                crosshairs: [
                    {
                        width: 1,
                        dashStyle: 'dash',
                        color: '#898989'
                    },
                    {
                        width: 1,
                        dashStyle: 'dash',
                        color: '#898989'
                    }
                ],
                headerFormat: '<div class="header">{point.key}</div>',
                pointFormat: '<div class="line"><div class="circle" style="background-color:{series.color};float:left;margin-left:10px!important;clear:left;"></div><p class="country" style="float:left;">{series.name}</p><p>{point.y:,.0f} {series.tooltipOptions.valueSuffix} </p></div>',
                borderWidth: 1,
                borderRadius: 5,
                borderColor: '#a4a4a4',
                shadow: false,
                useHTML: true,
                percentageDecimals: 2,
                backgroundColor: "rgba(255,255,255,.7)",
                style: {
                    padding: 0
                },
                shared: true

            },
            */
            useHighStocks: true,
            annotationsOptions: {
                enabledButtons: true,
                /*
                buttonsOffsets: [0, 0],
                buttons: [
                    {
                        size: 20,
                        symbol: { // button symbol options
                        shape: 'rect', // shape, taken from Highcharts.symbols
                        size: 12,
                        style: {
                            'stroke-width':  2,
                            'stroke': 'black',
                            fill: 'red',
                            zIndex: 121
                        }

                    },
                        states: { // states for button
                        selected: {
                            fill: '#9BD'
                        },
                        hover: {
                            fill: '#9BD'
                        }
                    },
                    annotationEvents: {
                        //start: $scope.annotateStep,
                        step: $scope.annotateStep, // to be called during mouse drag for new annotation
                        stop: $scope.annotateStop  // to be called after mouse up / release
                    },

                    annotation: { // standard annotation options, used for new annotation
                        linkedTo: $scope.title,
                        xValueEnd: 1413331200000,
                        yValueEnd: 136,
                        //xValueEnd: 0,
                        //yValueEnd: 0,
                        anchorX: 'left',
                        anchorY: 'top',
                        xAxis: 0,
                        yAxis: 0,
                        shape: {
                            type: 'path',
                        }
                    },

                    }

                ]
                */
                    /*
                    annotationEvents: {
                        step: $scope.callback, // to be called during mouse drag for new annotation
                        //stop: callback  // to be called after mouse up / release
                    },

                    symbol: { // button symbol options
                        shape: 'rect', // shape, taken from Highcharts.symbols
                        size: 12,
                        style: {
                            'stroke-width':  2,
                            'stroke': 'black',
                            fill: 'red',
                            zIndex: 121
                        }
                    },

                    states: { // states for button
                        selected: {
                            fill: '#9BD'
                        },
                        hover: {
                            fill: '#9BD'
                        }
                    },
                    style: { // button style itself
                        fill: 'black',
                        stroke: 'blue',
                        strokeWidth: 2,
                    },
                    size: 12, // button size


                }]
*/
            },
            annotations: $scope.annotations
                /*
            [{
                linkedTo: $scope.title,
                xValue: 1413331200000,
                yValue: 136,
                xValueEnd: 1413763200000,
                yValueEnd: 140,
                //allowDragY: false,
                //allowDragX: false,
                //anchorX: "left",
                //anchorY: "top",
                shape: {
                    type: 'path'
                }
            }]*/
            ,

        },
        series: [
            {
                id: $scope.ticker,
                name: 'Notifications',
                data: [], //$scope.chartdata,//[[1426204800000,10, 15, 8, 9]],
                type: 'candlestick',
                yAxis: 0,
                color: '#80a3ca'
            }
        ],


      //  ]
/*
        options: {
            chart: {
                type: 'candlestick',
                zoomType: 'x'
            }
        },
        series: [{
            type : 'candlestick',
            name : 'Stock Price',
            data: [ 1437479072, 15, 12, 8, 7],
            dataGrouping : {
                    units : [
                        [
                            'week', // unit name
                            [1] // allowed multiples
                        ], [
                            'month',
                            [1, 2, 3, 4, 6]
                        ]
                    ]
                }
        }],
        title: {
            text: 'Hello'
        },
        xAxis: {currentMin: 0, currentMax: 10, minRange: 1},
        loading: false,
        useHighStocks: true,
        /*
        annotations: [{
            xValue: 4,
            yValue: 125,
            title: {
                text: "Annotated chart!"
        }
      }]*/
    }

    $scope.getannotations = function(){
        $.ajax({
            url: '/getannotations/'+$scope.title,
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $.each(data.Annotations, function(e,o){
                    $scope.annotations.push(o);

                });
                $scope.$apply();
            }
        });
    }

    $scope.saveannotations = function(){
        var a = $('.highcharts-container').parent().highcharts().annotations.allItems;
        $.each(a, function(e,o){

            $scope.annotations.push(
                {
                    linkedTo: 'TEL.OL',
                    xValue: o.options.xValue,
                    yValue: o.options.yValue,
                    xValueEnd: o.options.xValueEnd,
                    yValueEnd: o.options.yValueEnd,
                    shape: {
                        type: 'path'
                    }
                });
        });
        //$scope.annotations = a;
        //$scope.$apply();

        $.ajax({
            url: '/saveannotations/'+$scope.title,
            data: JSON.stringify({ 'annotations': $scope.annotations }),
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
            }
        });

    }

    $scope.removeannotations = function(){
        $scope.annotations = [];
    }
}