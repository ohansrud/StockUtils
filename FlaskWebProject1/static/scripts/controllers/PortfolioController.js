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
    $scope.portfolio = {};

    $scope.getportfolio = function(){
        $.ajax({
            url: '/api/portfolio/',
            type: 'GET',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $scope.portfolio = JSON.parse( data.portfolio );

                $scope.$apply();
            }
        });
    };

    $scope.sellposition = function(position){
        $.ajax({
            url: '/api/portfolio/sell/'+position.ticker,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function (data) {
                if(!data.Success){
                    alert(data['error']);
                }else{
                    $scope.portfolio = JSON.parse( data.portfolio );
                    $scope.$apply();

                    alert("Sold from portfolio");
                }
            }
        });
    };
}