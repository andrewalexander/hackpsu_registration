'use strict';

app = angular.module('myApp.thanks', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/thanks/:action', {
    templateUrl: 'app/components/thanks/thanks.html',
    controller: 'ThanksCtrl'
  });
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
app.controller('ThanksCtrl', ['$scope', '$routeParams', function($scope, $routeParams) {
    $scope.action = $routeParams.action

}]);