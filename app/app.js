'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('myApp', [
  'ngRoute',
  'ngResource',
  'myApp.home',
  'myApp.version',
  'myApp.students'
])
.config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/home'});
}])
.controller('MainController', function($scope, $route, $routeParams, $location, $resource) {
     $scope.$route = $route;
     $scope.$location = $location;
     $scope.$routeParams = $routeParams;
     $scope.$resource = $resource;
 });