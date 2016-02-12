'use strict';

angular.module('myApp.home', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {
    templateUrl: 'app/components/home/home.html',
    controller: 'HomeCtrl'
  });
}])

.controller('HomeCtrl', function($scope, $routeParams, $http) {
    $scope.getVal = function() {
        $http.get("http://127.0.0.1:5000/login/hah").
            success(function(data){
                $scope.data = data;
            })
    }
    $scope.name = "HomeCtrl"
});