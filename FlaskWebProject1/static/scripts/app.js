/**
 * Created by t846432 on 20.07.2015.
 */


'use strict';
/*
function TickerCtrl($scope , $routeParams) {
    //alert("ticker");
    //alert($routeParams.ticker);
    $scope.title = "TEL.OL";
    $scope.loading = false;

}
*/

var app = angular.module("app", ['ngRoute', 'highcharts-ng']);
//Assign controllers to app
app.controller("ChartController", ['$scope', '$http' ,ChartController]);
//app.controller("TickerCtrl", ['$scope', '$http' ,TickerCtrl]);
app.controller("MainController", ['$scope', '$http' ,MainController]);

//Assign routing
app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: '/templates/home.html',
			controller: MainController
		})
		.when('/chart/:ticker', {
			templateUrl: '/templates/chart.html',
			controller: ChartController
		})
		.when('/chart/', {
			templateUrl: '/templates/chart.html',
			controller: ChartController
		});
			/*
		.otherwise({
			templateUrl: '/templates/home.html',
			controller: MainController
		});
		*/
		//$locationProvider.html5Mode(true);
}]);


