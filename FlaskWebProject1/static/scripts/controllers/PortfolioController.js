/**
 * Created by ohansrud on 8/5/15.
 */
function PortfolioController($scope ) {
    $scope.positions = [
        {
            "ticker": "BAKKA.OL",
            buy_date: "2015-07-30",
            buy_price: 100
        }

    ];

    $scope.getportfolio = function(){
        $.ajax({
            url: '/api/portfolio/',
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $scope.positions = data.positions;

                $scope.$apply();
            }
        });
    };
}