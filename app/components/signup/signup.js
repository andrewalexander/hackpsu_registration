'use strict';

angular.module('myApp.signup', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/signup/:id', {
    templateUrl: 'app/components/signup/signup.html',
    controller: 'SignUpCtrl'
  });
}])

.controller('SignUpCtrl', ['$routeParams', function($routeParams) { 
    console.log($routeParams.id)
}]);