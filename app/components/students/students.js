'use strict';

angular.module('myApp.students', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/students', {
    templateUrl: 'components/students/students.html',
    controller: 'StudentsCtrl'
  });
}])

.controller('StudentsCtrl', [function() { 
    // $scope.master = {};

    // $scope.update = function(user) {
    //     $scope.master = angular.copy(user);
    // };

    // $scope.reset = function() {
    //     $scope.user = angular.copy($scope.master);
    // };

    // $scope.reset();
}]);