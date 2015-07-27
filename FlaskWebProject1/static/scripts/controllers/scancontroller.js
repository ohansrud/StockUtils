/**
 * Created by t846432 on 27.07.2015.
 */
function ScanController($scope, $routeParams ) {

    $scope.findings = [];
    $scope.scanning = false;
    $scope.scanners = ["RSI70", "Doublecross","OBV"]
    $scope.scanner = {};

    $scope.scan = function(){
        $scope.scanning = true;
        $.ajax({
            url: '/api/scan/'+$scope.scanner,
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $.each(data, function(e,o){
                    console.log(o);
                    $scope.findings = o;
                });


                $scope.scanning = false;
                $scope.$apply();
                /*
                $.each(data.Annotations, function(e,o){
                    $scope.annotations.push(o);



                */
            }
        });
    }
}