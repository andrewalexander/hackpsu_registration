'use strict';

angular.module('myApp.signup', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/signup', {
    templateUrl: 'components/signup/signup.html',
    controller: 'SignUpCtrl'
  });
}])

.controller('SignUpCtrl', [function() { 
    
}]);