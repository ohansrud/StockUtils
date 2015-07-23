$(function() {
    function t() {
        function t() {
            var t = this.value,
                e = -1,
                i = $("#chart").highcharts();
            $.each(i.indicators.allItems, function(i, o) {
                o.options.type == t && (e = i)
            }), -1 == e && i.addIndicator({
                id: "AAPL",
                type: t,
                styles: {
                    "stroke-width": 1,
                    dashstyle: "solid"
                }
            })
        }
        var i = this;
        if (n(), i.options.addEvents) {
            {
                e(this)
            }
            h.change(t);
            var o = $("#highcharts-restart-tutorial").click(function() {
                $("#hello-msg-box").show(), $("#tooltip-mask-top").css({
                    height: "100%",
                    left: 0,
                    width: "100%"
                }).show()
            });
            i.options.showTooltip && o.click(), $("#highcharts-save").click(function() {
                var t = $("#chart").highcharts(),
                    e = [],
                    i = [];
                $.each(t.indicators.allItems, function(t, e) {
                    i.push({
                        id: e.options.id,
                        type: e.options.type,
                        params: e.options.params,
                        styles: e.options.styles,
                        yAxis: e.options.yAxis
                    })
                }), $.each(t.annotations.allItems, function(t, i) {
                    e.push(i.options)
                }), window.localStorage.setItem("data", JSON.stringify({
                    data: t.series[0].options.data,
                    indicators: i,
                    annotations: e
                }))
            }), $("#highcharts-reset").click(function() {
                var t = $("#chart").highcharts();
                window.localStorage.removeItem("data"), t.showLoading(), $.getJSON("http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-ohlcv.json&callback=?", function(e) {
                    c.series[0].data = e, c.showTooltip = !1, c.addEvents = !1, c.indicators = [], c.annotations = [], t.hideLoading(), $("#chart").highcharts("StockChart", $.extend(!0, {}, c), function(t) {
                        t.series[0].points[Math.round(t.series[0].points.length / 2)].firePointEvent("click")
                    })
                })
            }), $("#highcharts-sources").change(function() {
                var t = this.value,
                    e = $("#chart").highcharts();
                e.showLoading(), $("#chart-details").highcharts().series[0].setData([]), $.getJSON("http://www.highcharts.com/samples/data/jsonp.php?filename=" + t + ".json&callback=?", function(i) {
                    e.series[0].update({
                        data: i,
                        name: t.split("-")[0].toUpperCase()
                    }), e.hideLoading()
                })
            }), $("#highcharts-change-annotation").click(function() {
                var t = $("#chart").highcharts(),
                    e = t.annotationToEdit;
                e && e.options && (e.update(e.options.title && "" !== e.options.title.text ? Highcharts.merge(e.options, {
                    title: {
                        text: l.title.val()
                    }
                }) : Highcharts.merge(e.options, {
                    shape: {
                        params: {
                            stroke: l.border.css("background-color"),
                            fill: l.fill.css("background-color")
                        }
                    }
                })), e.redraw()), l.container.hide(), t.annotationToEdit = !1
            }), $(l.container).find(".cancel").click(function(t) {
                var e = $("#chart").highcharts(),
                    i = e.annotationToEdit;
                i && i.options && i.events.deselect.call(i, t), l.container.hide(), e.annotationToEdit = !1
            }), $("#highcharts-remove-annotation").click(function() {
                var t = $("#chart").highcharts(),
                    e = t.annotationToEdit;
                e && e.options && e.destroy(), l.container.hide(), t.annotationToEdit = !1
            }), $("#highcharts-change-fill").ColorPicker({
                color: "#e7f0f9",
                livePreview: !0,
                onShow: function(t) {
                    return $(t).fadeIn(500), !1
                },
                onHide: function(t) {
                    return $(t).fadeOut(500), !1
                },
                onChange: function(t, e) {
                    $("#highcharts-change-fill").css("backgroundColor", "#" + e)
                }
            }), $("#highcharts-change-border").ColorPicker({
                color: "#6688aa",
                livePreview: !0,
                onShow: function(t) {
                    return $(t).fadeIn(500), !1
                },
                onHide: function(t) {
                    return $(t).fadeOut(500), !1
                },
                onChange: function(t, e) {
                    $("#highcharts-change-border").css("backgroundColor", "#" + e)
                }
            }), $("#hello-msg-box .tooltip-close").click(function() {
                $("#hello-msg-box").hide(), $("#tooltip-mask-top").hide()
            }), $("#hello-msg-box .hello-start-tutorial").click(function() {
                $("#hello-msg-box").hide(), r = new a("#tooltip", s()).start()
            })
        }
    }

    function e() {
        $("#chart-details").highcharts({
            chart: {
                marginRight: 30
            },
            annotationsOptions: {
                buttons: []
            },
            title: {
                useHTML: !0,
                align: "left",
                y: 0,
                text: '<div style="width:400px; text-align: center; background-color: #f2f2f2; font-size:14px; padding:10px 0px 5px 0px;">Zoom view</div>'
            },
            yAxis: {
                lineWidth: 1,
                lineColor: "#696969",
                gridLineColor: "#e6e6e6",
                minRange: 100,
                title: {
                    text: null
                }
            },
            xAxis: {
                lineWidth: 1,
                lineColor: "#696969",
                gridLineColor: "#e6e6e6",
                type: "datetime"
            },
            credits: {
                enabled: !1
            },
            legend: {
                enabled: !1
            },
            tooltip: {
                enabled: !1
            },
            plotOptions: {
                series: {
                    states: {
                        hover: {
                            halo: {
                                size: 0
                            }
                        }
                    },
                    cursor: "ns-resize",
                    point: {
                        events: {
                            drag: function(t) {
                                {
                                    var e, i, o, a, s = this.series.chart,
                                        n = this.series,
                                        r = $("#chart").highcharts().series[0],
                                        h = (r.xData.indexOf(t.newX), r.chart.getSelectedPoints()),
                                        l = h[h.length - 1],
                                        c = r.processedXData.indexOf(s.pointToSelect.x);
                                    t.target
                                }
                                c >= 0 && l && (e = 3 * (c + 1) - 1, i = n.yData.reduce(function(t, e) {
                                    return t + e
                                }), o = i / n.yData.length, a = r.yAxis.toPixels(o) - r.chart.plotTop, l.graphic && (a > 0 && a < r.yAxis.height ? (l.graphic.translate(0, a - l.plotY), l.graphic.show()) : l.graphic.hide()), r.graphPath[e] = a, r.graph.attr({
                                    d: r.graphPath
                                }))
                            },
                            drop: function(t) {
                                var e = this.series.chart,
                                    i = t.target,
                                    o = $("#chart").highcharts().series[0],
                                    a = o.xData.indexOf(i.x),
                                    s = o.processedXData.indexOf(e.pointToSelect.x);
                                a >= 0 && (o.options.data[a][1] = i.y, o.isDirty = o.isDirtyData = chart.isDirtyBox = !0, o.options.data[a][1] > o.options.data[a][2] ? o.options.data[a][2] = o.options.data[a][1] : o.options.data[a][1] < o.options.data[a][3] && (o.options.data[a][3] = o.options.data[a][1]), o.setData(o.options.data, !0, !0), s >= 0 && o.points[s].select(!0))
                            }
                        }
                    },
                    stickyTracking: !1
                }
            },
            series: [{
                draggableY: !0,
                data: []
            }]
        }, o)
    }

    function o() {
        var t, e, i = $("#chart-details"),
            o = i.find(".highcharts-title"),
            a = $("#chart").highcharts(),
            s = Math.round(a.series[0].points.length / 2),
            n = !1;
        o.mousedown(function(o) {
            var a = i.offset();
            n = !0, t = o.pageX - a.left, e = o.pageY - a.top
        }), $(document).mousemove(function(o) {
            n && i.css({
                top: o.pageY - e + "px",
                left: o.pageX - t + "px"
            })
        }), $(document).mouseup(function() {
            n = !1
        }), a.series[0].setData(a.series[0].options.data, !0, !1), a.series[0].points[s].firePointEvent("click"), a.tooltip.refresh(a.series[0].points[s])
    }

    function a(t, e) {
        var i = this;
        return this.tooltip = $(t), this.actual = this.tooltip.find(".tooltip-actual"), this.max = this.tooltip.find(".tooltip-max"), this.content = this.tooltip.find(".tooltip-content"), this.nextButton = this.tooltip.find(".tooltip-next"), this.prevButton = this.tooltip.find(".tooltip-prev"), this.endButton = this.tooltip.find(".tooltip-end"), this.masks = [$("#tooltip-mask-top"), $("#tooltip-mask-right"), $("#tooltip-mask-bottom"), $("#tooltip-mask-left"), $("#tooltip-mask-center")], this.messages = e, this.arrow = $("#tooltip .diamond"), this.messagesLength = this.messages.length, this.index = 0, i.start = function() {
            return i.prevButton.click(i.prev).hide(), i.nextButton.click(i.next), i.endButton.click(i.stop), i.tooltip.find(".tooltip-close").click(i.stop), i.tooltip.find(".tooltip-max").text(i.messagesLength), i.allowReflow = !0, i.show(), i
        }, i.next = function() {
            return i.index < i.messagesLength - 1 && (i.index++, i.show(!0)), i
        }, i.prev = function() {
            return i.index > 0 && (i.index--, i.show(!0)), i
        }, i.stop = function() {
            return i.tooltip.fadeOut(), i.allowReflow = !1, $.each(i.masks, function(t, e) {
                e.fadeOut()
            }), i
        }, i.show = function() {
            {
                var t = i.messages[i.index],
                    e = $(t.relativeTo),
                    o = e.offset(),
                    a = o.top + 20,
                    s = t.pane.padding,
                    n = t.offset ? t.offset.top : 0,
                    r = t.pane.marginTop || 0,
                    h = t.pane.offsetLeft || 0,
                    l = t.pane.marginLeft || 0,
                    c = t.pane.boxWidth || 200;
                o.left > 50 ? o.left - 50 : o.left
            }
            return o.left += h, i.tooltip.width(c), i.masks[0].css({
                width: t.pane.width + 2 * s + "px",
                height: a - 20 - s + r + "px",
                left: o.left - s - 5 + "px"
            }), i.masks[1].css({
                left: o.left + t.pane.width + s - 5 + "px"
            }), i.masks[2].css({
                width: t.pane.width + 2 * s + "px",
                top: a + t.pane.height - s - 20 + "px",
                left: o.left - s - 5 + "px"
            }), i.masks[3].css({
                width: o.left - s - 5 + "px"
            }), i.masks[4].css({
                width: t.pane.width + 2 * s + "px",
                height: t.pane.height - r + "px",
                top: a - s - 20 + r + "px",
                left: o.left - s - 5 + "px"
            }), $.each(i.masks, function(t, e) {
                e.show()
            }), 0 === i.index ? i.prevButton.hide() : i.prevButton.show(), i.index == i.messagesLength - 1 ? (i.nextButton.hide(), i.prevButton.hide(), i.endButton.show()) : (i.nextButton.show(), i.prevButton.show(), i.endButton.hide()), i.content.html(t.text), i.actual.text(i.index + 1), "left" == t.arrowPosition ? (i.tooltip.css({
                left: o.left + t.pane.width + s + 7 + l + "px",
                top: a + n + "px"
            }), i.arrow.css({
                left: "-7px",
                top: i.tooltip.height() / 2 - 7 + "px"
            }).show()) : "top" == t.arrowPosition ? (i.tooltip.css({
                left: l + o.left - s - 13 - (i.tooltip.width() - t.pane.width - 20) / 2 + "px",
                top: a + s + 15 + "px"
            }), i.arrow.css({
                left: i.tooltip.width() / 2 - 7 + "px",
                top: "-7px"
            }).show()) : (i.tooltip.css({
                left: l + e.width() * parseFloat(t.pane.left) / 100 + "px",
                top: "45%"
            }), i.arrow.hide()), i.tooltip.show(), i
        }, i.reflow = function() {
            i.show(!1)
        }, this
    }

    function s() {
        return [{
            text: '<div class="tooltip-title">Source</div><div class="tooltip-subcontent">We can plug in real-time data stream, CSV files or any other data source, Yahoo finance for example.</div>',
            relativeTo: "#highcharts-sources",
            arrowPosition: "top",
            pane: {
                marginTop: -6,
                padding: 3,
                width: 96,
                height: 30
            }
        }, {
            text: '<div class="tooltip-title">Save & Reset</div><div class="tooltip-subcontent">We can make the chart save into your database or any other storage so you can get back to it anytime.</div>',
            relativeTo: "#highcharts-manage-chart",
            arrowPosition: "top",
            pane: {
                marginTop: -6,
                padding: 3,
                width: 175,
                height: 32
            }
        }, {
            text: '<div class="tooltip-title">Indicators</div><div class="tooltip-subcontent">We can prepare special series. For example, they can be drawn based on calculations made using other series.</div>',
            relativeTo: "#highcharts-indicators",
            arrowPosition: "top",
            pane: {
                marginTop: -5,
                padding: 3,
                width: 96,
                height: 30
            }
        }, {
            text: '<div class="tooltip-title">Annotations</div><div class="tooltip-subcontent">You may be able to add many complex objects to your chart if we install one of our plugins. <span style="color: yellow;">Please use right-click to edit objects</span></div>',
            relativeTo: ".highcharts-button:eq(2)",
            arrowPosition: "top",
            pane: {
                marginTop: -5,
                offsetLeft: -35,
                padding: 3,
                width: 139,
                height: 32
            }
        }, {
            text: '<div class="tooltip-title">Draggable</div><div class="tooltip-subcontent">Many custom and complex features can be added. Using drag and drop method to manipulate data is an example. Please drag one of these points to see real-time changes in a main series.</div>',
            relativeTo: "#chart-details",
            arrowPosition: "left",
            pane: {
                offsetLeft: 5,
                padding: 15,
                height: 278,
                width: 400
            }
        }, {
            text: '<div class="tooltip-title">Thank you</div><div class="tooltip-subcontent">Now you can play with this chart and try it yourself.</div>',
            relativeTo: "body",
            arrowPosition: "none",
            endButton: !0,
            pane: {
                left: "50%",
                marginLeft: -155,
                padding: 0,
                height: 0,
                width: 0,
                boxWidth: "310px"
            }
        }]
    }

    function n() {
        var t = $(".highcharts-button:eq(3)"),
            e = t.offset(),
            i = $("#menu-nav"),
            o = i.width();
        i.css({
            top: e.top,
            left: e.left - o - 14,
            display: "block"
        }), r && r.allowReflow && r.reflow()
    }
    console.info("See email."), Highcharts.Tooltip.prototype.hide = function() {}, Highcharts.theme = {
        yAxis: {
            lineWidth: 1,
            lineColor: "#696969",
            gridLineColor: "#e6e6e6"
        },
        navigator: {
            yAxis: {
                lineColor: "#b2b1b6"
            }
        },
        xAxis: {
            lineWidth: 1,
            lineColor: "#696969",
            tickLength: 5,
            tickColor: "#696969",
            gridLineColor: "#e6e6e6",
            gridLineWidth: 1
        }
    }, Highcharts.setOptions(Highcharts.theme);
    var r, h = $("#highcharts-indicators"),
        l = {
            container: $("#highcharts-edit-annotation"),
            fill: $("#highcharts-change-fill"),
            border: $("#highcharts-change-border"),
            title: $("#highcharts-change-title")
        },
        c = {
            showTooltip: !1,
            addEvents: !0,
            chart: {
                panning: !1,
                borderWidth: 5,
                borderColor: "#e8eaeb",
                borderRadius: 0,
                backgroundColor: "#f2f2f2",
                height: $(window).height(),
                events: {
                    load: t,
                    redraw: function() {
                        if (this.selectedXPoint) {
                            var t = this.series[0],
                                e = t.processedXData,
                                o = t.xData.indexOf(this.selectedXPoint),
                                a = t.processedXData.indexOf(this.selectedXPoint),
                                s = e.length,
                                r = !1;
                            if (i = 0, o >= 0 && this.series[0].points[o]) t.points[o].select(!0), r = !0;
                            else if (a >= 0) t.points[a].select(!0), r = !0;
                            else
                                for (; i < s; i++)
                                    if (e[i] > this.selectedXPoint) {
                                        t.points[i].select(!0), r = !0;
                                        break
                                    }
                            r || t.points[Math.round(s / 2)].select(!0)
                        }
                        setTimeout(n, 10);
                        var h = this.yAxis,
                            l = this.renderer,
                            c = this.plotWidth;
                        Highcharts.each(h, function(t) {
                            "navigator-y-axis" !== t.options.id && (t.backgroundPane && t.backgroundPane.destroy(), t.backgroundPane = l.rect(t.left, t.top, c, t.height).attr({
                                fill: "#fff",
                                zIndex: 0
                            }).add())
                        });
                        var d = this.scroller,
                            p = d.yAxis.height;
                        d.rightCustomLine && d.rightCustomLine.destroy(), d.rightCustomLine = l.path(["M", d.scrollerLeft + d.scrollerWidth - 1, d.top, "L", d.scrollerLeft + d.scrollerWidth - 1, d.top + p]).attr({
                            "stroke-width": 1,
                            stroke: "#b2b1b6",
                            "shape-rendering": "crispEdges"
                        }).add()
                    }
                }
            },
            credits: {
                enabled: !1
            },
            xAxis: {
                minRange: 31536e6
            },
            rangeSelector: {
                buttonTheme: {
                    fill: "#ffffff",
                    stroke: "#cccccc",
                    "stroke-width": 1,
                    states: {
                        hover: {
                            fill: "#99bbdd"
                        }
                    }
                },
                selected: 2,
                buttons: [{
                    type: "month",
                    count: 6,
                    text: "6m"
                }, {
                    type: "year",
                    count: 1,
                    text: "1y"
                }, {
                    type: "year",
                    count: 2,
                    text: "2y"
                }, {
                    type: "year",
                    count: 5,
                    text: "5y"
                }, {
                    type: "all",
                    text: "All"
                }]
            },
            indicators: [{
                id: "AAPL",
                type: "sma",
                params: {
                    period: 14
                },
                styles: {
                    "stroke-width": 1,
                    stroke: "#8ddd54",
                    dashstyle: "solid"
                }
            }, {
                id: "AAPL",
                type: "rsi",
                params: {
                    period: 14,
                    overbought: 70,
                    oversold: 30
                },
                styles: {
                    "stroke-width": 1,
                    stroke: "#6ba583",
                    dashstyle: "solid"
                },
                yAxis: {
                    title: {
                        text: "RSI"
                    }
                }
            }],
            yAxis: {
                opposite: !1,
                title: {
                    text: "DATA SMA EMA"
                },
                labels: {
                    align: "left",
                    x: 2
                }
            },
            tooltip: {
                crosshairs: !1,
                shared: !1,
                enabledIndicators: !0,
                followPointer: !1,
                backgroundColor: "white",
                borderWidth: 0,
                borderRadius: 0,
                shape: "square",
                headerFormat: "{point.key} ",
                pointFormat: ' | <span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b>',
                formatter: function() {
                    var t, e, i = this.x,
                        o = this.series,
                        a = "";
                    return t = o.currentDataGrouping ? o.tooltipOptions.dateTimeLabelFormats[o.currentDataGrouping.unitName] : o.tooltipOptions.dateTimeLabelFormats.day, a += Highcharts.dateFormat(t, i), a += '| <span style="color:' + o.color + '">' + o.name + "</span>: <b>" + this.y.toFixed(2) + "</b>", o.indicators && $.each(o.indicators, function(t, o) {
                        e = o.xData ? o.xData.indexOf(i) : -1, e >= 0 && (a += ' | <span style="color:' + o.graph.stroke + '">' + o.options.type.toUpperCase() + "</span>: <b>" + o.yData[e].toFixed(2) + "</b>")
                    }), a
                },
                positioner: function() {
                    return {
                        x: 70,
                        y: 50
                    }
                }
            },
            annotationsOptions: {
                events: {
                    contextmenu: function(t) {
                        var e, i = l.container.width(),
                            o = $("body").width(),
                            a = t.pageY,
                            s = i + t.pageX > o ? o - i : t.pageX;
                        this.options.shape.params ? (l.border.css({
                            "background-color": this.options.shape.params.stroke
                        }), l.fill.css({
                            "background-color": this.options.shape.params.fill
                        })) : l.title.val(this.options.title.text), this.options.title && "" !== this.options.title.text ? (l.container.find(".without-title").hide(), l.container.find(".with-title").show()) : (l.container.find(".without-title").show(), l.container.find(".with-title").hide()), l.container.css({
                            top: a + "px",
                            left: s + "px"
                        }).show(), this.chart.annotationToEdit = this, e = l.container.find("input:visible")[0], e && e.focus(), t.preventDefault()
                    }
                }
            },
            annotations: [],
            navigator: {
                xAxis: {
                    plotBands: [{
                        color: "#fff",
                        from: -1 / 0,
                        to: 1 / 0
                    }]
                }
            },
            series: [{
                lineWidth: 2,
                cropThreshold: 0,
                id: "AAPL",
                name: "AAPL",
                data: [],
                tooltip: {
                    valueDecimals: 2
                },
                dataGrouping: {
                    groupPixelWidth: 40
                },
                allowPointSelect: !0,
                marker: {
                    enabled: !0,
                    radius: .1,
                    states: {
                        select: {
                            enabled: !0,
                            radius: 5
                        }
                    }
                },
                point: {
                    events: {
                        select: function() {
                            for (var t, e, i, o = this, a = o.x, s = o.series.currentDataGrouping, n = s && s.totalRange > 864e5 ? a + s.totalRange - 1 : a, r = $("#chart-details").highcharts(), h = o.series.xData, l = h.length, c = [], d = 0, p = []; l > d; d++) h[d] >= a && (h[d] <= n ? (i = o.series.yData[d], p.push(i), c.push([h[d], i])) : d = l);
                            r.pointToSelect = {
                                x: o.x
                            }, t = .9 * Math.min.apply(null, p), e = 1.1 * Math.max.apply(null, p), r.series[0].update({
                                data: c
                            }, !1), r.yAxis[0].setExtremes(t, e), o.series.chart.selectedXPoint = o.x
                        }
                    }
                }
            }]
        },
        d = window.localStorage.getItem("data");
    if (d) {
        var p = JSON.parse(d);
        c.series[0].data = p.data, c.annotations = p.annotations, c.indicators = p.indicators, $("#chart").highcharts("StockChart", $.extend(!0, {}, c))
    } else $.getJSON("http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-ohlcv.json&callback=?", function(t) {
        c.series[0].data = t, $("#chart").highcharts("StockChart", $.extend(!0, {}, c))
    })
});