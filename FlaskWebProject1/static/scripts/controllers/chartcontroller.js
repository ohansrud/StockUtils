var utils = {
	getRadius: function(e) {
		var ann = this,
			chart = ann.chart,
			bbox = chart.container.getBoundingClientRect(),
			x = e.clientX - bbox.left,
			y = e.clientY - bbox.top,
			xAxis = chart.xAxis[ann.options.xAxis],
			yAxis = chart.yAxis[ann.options.yAxis],
			dx = Math.abs(x - xAxis.toPixels(ann.options.xValue)),
			dy = Math.abs(y - yAxis.toPixels(ann.options.yValue));
			radius = parseInt(Math.sqrt(dx * dx + dy * dy), 10);
		ann.shape.attr({
			r: radius
		});
		return radius;
	},
	getRadiusAndUpdate:	function(e) {
		var r = utils.getRadius.call(this, e);
		this.update({
			shape: {
				params: {
					r: r,
					x: -r,
					y: -r
				}
			}
		});
	},
	getPath: function(e) {
		var ann = this,
			chart = ann.chart,
			bbox = chart.container.getBoundingClientRect(),
			x = e.clientX - bbox.left,
			y = e.clientY - bbox.top,
			xAxis = chart.xAxis[ann.options.xAxis],
			yAxis = chart.yAxis[ann.options.yAxis],
			dx = x - xAxis.toPixels(ann.options.xValue),
			dy = y - yAxis.toPixels(ann.options.yValue);

		var path = ["M", 0, 0, 'L', Math.round(parseInt(dx, 10)), Math.round(parseInt(dy, 10))];
		ann.shape.attr({
			d: path
		});

		return path;
	},
	getPathAndUpdate: function(e) {
		var ann = this,
			chart = ann.chart,
			path = utils.getPath.call(ann, e),
			xAxis = chart.xAxis[ann.options.xAxis],
			yAxis = chart.yAxis[ann.options.yAxis],
			x = xAxis.toValue(path[4] + xAxis.toPixels(ann.options.xValue)) ,
			y = yAxis.toValue(path[5] + yAxis.toPixels(ann.options.yValue)) ;

		this.update({
			xValueEnd: x,
			yValueEnd: y,
			shape: {
				params: {
					d: path
				}
			}
		});
	},
	getRect: function(e) {
		var ann = this,
			chart = ann.chart,
			bbox = chart.container.getBoundingClientRect(),
			x = e.clientX - bbox.left,
			y = e.clientY - bbox.top,
			xAxis = chart.xAxis[ann.options.xAxis],
			yAxis = chart.yAxis[ann.options.yAxis],
			sx = xAxis.toPixels(ann.options.xValue),
			sy = yAxis.toPixels(ann.options.yValue),
			dx = x - sx,
			dy = y - sy,
			w = Math.round(dx) + 1,
			h = Math.round(dy) + 1,
			ret = {};

		ret.x = w < 0 ? w : 0;
		ret.width = Math.abs(w);
		ret.y = h < 0 ? h : 0;
		ret.height = Math.abs(h);

		ann.shape.attr({
			x: ret.x,
			y: ret.y,
			width: ret.width,
			height: ret.height
		});
		return ret;
	},
	getRectAndUpdate: function(e) {
		var rect = utils.getRect.call(this, e);
		this.update({
			shape: {
				params: rect
			}
		});
	},
	getText: function(e) {
		// do nothing
	},
	showInput: function(e) {
		var ann = this,
				chart = ann.chart,
				index = chart.annotationInputIndex = chart.annotationInputIndex ? chart.annotationInputIndex : 1,
				input =  document.createElement('span'),
				button;

		input.innerHTML = '<input type="text" class="annotation-' + index + '" placeholder="Add text"><button class=""> Done </button>';
		input.style.position = 'absolute';
		input.style.left = e.pageX + 'px';
		input.style.top = e.pageY + 'px';

		document.body.appendChild(input);
		input.querySelectorAll("input")[0].focus();
		button = input.querySelectorAll("button")[0];
		button.onclick = function() {
				var parent = this.parentNode;

				ann.update({
						title: {
								text: parent.querySelectorAll('input')[0].value
						}
				});
				parent.parentNode.removeChild(parent);
		};
		chart.annotationInputIndex++;
	}
}

function ChartController($scope, $routeParams ) {
    $scope.currentprice = 0;
    $scope.getPath= function(e) {
		var ann = this,
			chart = ann.chart,
			bbox = chart.container.getBoundingClientRect(),
			x = e.clientX - bbox.left,
			y = e.clientY - bbox.top,
			xAxis = chart.xAxis[ann.options.xAxis],
			yAxis = chart.yAxis[ann.options.yAxis],
			dx = x - xAxis.toPixels(ann.options.xValue),
			dy = y - yAxis.toPixels(ann.options.yValue);

		var path = ["M", 0, 0, 'L', Math.round(parseInt(dx, 10)), Math.round(parseInt(dy, 10))];
		ann.shape.attr({
			d: path
		});

		return path;
	};
    $scope.annotations = [];
    $scope.ticker = $routeParams.ticker;
    $scope.loading = true;
    $scope.loading_backtest = false;
    $scope.backtester = {};
    $scope.backtesting = [];
    $scope.gettickers = function(){
        $.ajax({
            url: '/api/tickers/',
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $scope.tickers = data.result;
                $scope.$apply();
            },
            complete: function (data) {
                notyMessage(data);
            },
        });
    };

    $scope.getchartdata = function(){
        //console.log($scope.chartConfig);
        //$scope.chartConfig.series[0].data.unshift([1426118400,10, 15, 8, 9]);
        //$scope.chartConfig.loading = true;
        $scope.loading = true;
        $.ajax({
            url: '/api/getchartdata/'+$scope.ticker,
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
                    $scope.currentprice = o[4];
                    $scope.chartConfig.series[0].data.push(
                        [Date.parse(o[0]), o[1], o[2], o[3], o[4]]

                    );
                    $scope.chartConfig.series[0].id = $scope.ticker;
                    $scope.chartConfig.series[0].name = $scope.ticker;

                    volume.push(
                        [Date.parse(o[0]), o[5]]
                    );
                    $scope.chartConfig.series[1].data = volume;
                    $scope.chartConfig.series[1].id = "Volume";
                    $scope.chartConfig.series[1].name = "Volume";
                });

                //$scope.chartConfig.series.push({
                //    data: ohlc
                //})

                //$scope.data.push(ohlc);
                $scope.$apply();
                //$('#container').highcharts().hideLoading();
                $scope.loading = false;
                $scope.getannotations();

            },
            complete: function (data) {
                notyMessage(data);
            },
        });
    };
    $scope.toggleLoading = function () {
        this.chartConfig.loading = !this.chartConfig.loading
    }
    $scope.groupingUnits = [[
                'week',                         // unit name
                [1]                             // allowed multiples
            ], [
                'month',
                [1, 2, 3, 4, 6]
            ]];
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
                enabled: true,
                selected: 1
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
                {
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
            useHighStocks: true,
            annotationsOptions: {
                buttons: [
                    {

                        annotationEvents: {
                            step:  $scope.getPath,
                            stop: utils.getPathAndUpdate
                        },
                        annotation: {
                            anchorX: 'left',
                            anchorY: 'top',
                            xAxis: 0,
                            yAxis: 0,
                            shape: {
                                type: 'path',
                                params: {
                                    d: ['M', 0, 0, 'L', 10, 10],
                                    fill: 'rgba(255,0,0,0.4)',
                                    stroke: 'black'
                                }
                            },
                            events: {
                                click: function(e){
                                    $scope.showing = false;
                                    $scope.$apply();
                                    console.log(e);
                                },
                                dblclick: function(e){
                                    this.destroy();
                                },
                                contextmenu: function(e){
                                    //alert("Menu!");
                                    //$('#constext-menu-div').css({top: e.chartY, left: e.chartX});
	                        	    //$('#constext-menu-div').show();
                                    $scope.showing = true;
                                    $scope.$apply();
	                        	    console.log(e);
                                    e.preventDefault()
                                }
                            }
                        },
                        symbol: {
                            shape: 'line',
                            size: 12,
                            style: {
                                'stroke-width':  2,
                                'stroke': 'black',
                                fill: 'red',
                                zIndex: 121
                            }
                        },
                        style: {
                            fill: 'black',
                            stroke: 'blue',
                            strokeWidth: 2
                        },
                        size: 12,
                        states: {
                            selected: {
                                fill: '#9BD'
                            },
                            hover: {
                                fill: '#9BD'
                            }
                        }

                    }

                ]

              }
            },
        annotations: [],//$scope.annotations,
        series: [
            {
                id: $scope.ticker,
                name: 'Notifications',
                data: [],
                type: 'candlestick',
                yAxis: 0,

                dataGrouping: {
                    units: $scope.groupingUnits
                }
            },
            {
                type: 'column',
                name: 'Volume',
                data: [],
                yAxis: 1,
                color: '#80a3ca',
                dataGrouping: {
                    units: $scope.groupingUnits
                }
            },
            {
                type: 'flags',
                name: 'Backtesting flags',
                data: [],
                onSeries: $scope.ticker,
                shape: 'squarepin'
            }
        ],



    }

    $scope.events= {
            click: function(e){
                $scope.showing = !$scope.showing;
                $scope.$apply();
                console.log(e);
                e.preventDefault()
            },
            dblclick: function(e){
                this.destroy();
            },
            contextmenu: function(e){
                //alert("Menu!");
                //$('#constext-menu-div').css({top: e.chartY, left: e.chartX});
                //$('#constext-menu-div').show();
                $scope.showing = true;
                $scope.$apply();
                console.log(e);
                e.preventDefault()
            }
        };

    $scope.getannotations = function(){
        $.ajax({
            url: '/api/getannotations/'+$scope.ticker,
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                var annotations = JSON.parse( data.Annotations );

                $.each(annotations, function(e,o){
                    //o.events= events;
                     var ev =
                        {
                            id: o.id,
                            anchorX: "left",
                            anchorY: "top",
                            linkedTo: $scope.ticker,
                            xValue: o.xValue,
                            yValue: o.yValue,
                            xValueEnd: o.xValueEnd,
                            yValueEnd: o.yValueEnd,
                            shape: {
                                params: {
                                  fill: "rgba(0,0,0,0)",
                                  stroke: "#000000",
                                },
                                type: 'path',
                            },
                            events: $scope.events

                        };

                    $('.highcharts-container').parent().highcharts().addAnnotation(ev);

                });
                $scope.$apply();
                //$('.highcharts-container').parent().highcharts().redrawAnnotations();
            },
            complete: function (data) {
                notyMessage(data);
            },
        });
    }
    $scope.saveannotations = function(){
        var a = $('.highcharts-container').parent().highcharts().annotations.allItems;
        //var subset = _(a).pick('options', 'shape');

        var annotations = [];
         $.each(a, function(e,o){

            annotations.push(
                {
                    id: o.options.id,
                    anchorX: "left",
                    anchorY: "top",
                    linkedTo: $scope.ticker,
                    //options: {
                        xValue: Math.round(o.options.xValue),
                        yValue: Math.round(o.options.yValue),
                        xValueEnd: Math.round(o.options.xValueEnd),
                        yValueEnd: Math.round(o.options.yValueEnd),
                    //},
                    shape: {
                        type: 'path'
                    }
                });
        });


        $.ajax({
            url: '/api/saveannotations/'+$scope.ticker,
            data: JSON.stringify({ 'annotations': annotations }),
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                if(data.Success)
                {
                    $scope.removeannotations();
                    var annotations = JSON.parse( data.result );
                    //Remove all annotations

                    //Redraw with new properties
                    $.each(annotations, function(e,o){
                    //o.events= events;
                     var ev =
                        {
                            id: o.id,
                            anchorX: "left",
                            anchorY: "top",
                            linkedTo: $scope.ticker,
                            xValue: o.xValue,
                            yValue: o.yValue,
                            xValueEnd: o.xValueEnd,
                            yValueEnd: o.yValueEnd,
                            shape: {
                                params: {
                                  fill: "rgba(0,0,0,0)",
                                  stroke: "#000000",
                                },
                                type: 'path',
                            },
                            events: $scope.events

                        };

                        $('.highcharts-container').parent().highcharts().addAnnotation(ev);

                    });
                }
            },
            complete: function (data) {
                notyMessage(data);
            },

        });



    }
    $scope.removeannotations = function(){

        var a = $('.highcharts-container').parent().highcharts().annotations.allItems;

        while(a.length>0){
            try{
                $.each(a, function(e,o){
                    o.destroy();
                });

            }catch(ex){}
        };

    }

    $scope.backtest = function(){
        $scope.loading_backtest = true;
        $.ajax({
            url: '/api/backtest/'+$scope.backtester +'/'+$scope.ticker,
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $scope.loading_backtest = false;
                var result = JSON.parse( data.result );
                $scope.backtesting = result.trades;
                $scope.chartConfig.series[2].data = [];
                //Add flags
                $.each($scope.backtesting, function(e,o){
                    $scope.chartConfig.series[2].data.push(
                    {
                        x: Date.parse(o.buy_date),
                        title: 'Buy:' + o.buy_price
                    });

                    $scope.chartConfig.series[2].data.push(
                    {
                        x: Date.parse(o.sell_date),
                        title: 'Sell:' + o.sell_price
                    });


                });

                $scope.$apply();
            },
            complete: function (data) {
                notyMessage(data);
            },
        });
    }
    $scope.getpeaks = function(){
        $.ajax({
            url: '/api/getpeaks/'+$scope.ticker,
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $scope.chartConfig.series[2].data = [];

                //Add flags
                $.each(data.results, function(e,o){
                    console.log(e);
                    console.log(o);
                    $scope.chartConfig.series[2].data.push({
                            x: Date.parse(o),
                            title: 'V'
                        })

                });

                $scope.$apply();
            },
            complete: function (data) {
                notyMessage(data);
            },
        });
    }
    $scope.showing = false;
    $scope.amount = 1;
    $scope.buyposition = function () {
        $.ajax({
            url: '/api/portfolio/buy/'+$scope.ticker,
            data: JSON.stringify({ 'amount': $scope.amount }),
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
            },
            complete: function (data) {
                notyMessage(data);
            },
        });
    }

}