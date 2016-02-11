'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('myApp', [
  'ngRoute',
  'myApp.home',
  'myApp.version',
  'myApp.students',
  'myApp.signup',
  'myApp.rsvp',
  'myApp.thanks',
  'myApp.exists'
])
.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
  $routeProvider.otherwise({redirectTo: '/home'});
  $httpProvider.defaults.useXDomain = true;
}])
.controller('MainController', function($scope, $route, $routeParams, $location, $http) {
     $scope.$route = $route;
     $scope.$location = $location;
     $scope.$routeParams = $routeParams;
 });