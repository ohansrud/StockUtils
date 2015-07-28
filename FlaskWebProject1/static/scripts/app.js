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
app.controller("ChartController", ['$scope', '$http', '$routeParams' ,ChartController]);
app.controller("ScanController", ['$scope', '$http', '$routeParams' ,ScanController]);
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
		.when('/scan/', {
			templateUrl: '/templates/scan.html',
			controller: ScanController
		})
			/*
		.when('/chart', {
			templateUrl: '/templates/chart.html',
			controller: ChartController
		})*/
		.otherwise({
			templateUrl: '/templates/home.html',
			controller: MainController
		});

		$locationProvider.html5Mode(true);
}]);

app.run([
  '$rootScope',
  function($rootScope) {
    // see what's going on when the route tries to change
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
      // next is an object that is the route that we are starting to go to
      // current is an object that is the route where we are currently
		try{
			//var currentPath = current.originalPath;
      		var nextPath = next.originalPath;
			console.log(nextPath);
		}catch(e){}
    });
  }
]);
