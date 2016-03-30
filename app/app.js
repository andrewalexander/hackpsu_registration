'use strict';

// Declare app level module which depends on views, and components
var app = angular.module('myApp', [
  'ngRoute',
  'myApp.admin',
  'myApp.home',
  'myApp.version',
  'myApp.students',
  'myApp.signin',
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
 // }).run(run);
});

// function run($http, $rootScope, $window) {
//     // add JWT token as default auth header
//     $http.defaults.headers.common['Authorization'] = 'Bearer ' + $window.jwtToken;

//     // update active tab on state change
//     $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
//         $rootScope.activeTab = toState.data.activeTab;
//     });
// }

// // manually bootstrap angular after the JWT token is retrieved from the server
// $(function () {
//     // get JWT token from server
//     $.get('/app/token', function (token) {
//         window.jwtToken = token;

//         angular.bootstrap(document, ['app']);
//     });
// });

$('input:checkbox').change(function(){
  if($(this).is('checked')) 
      $(this).parent().addClass('selected'); 
  else 
      $(this).parent().removeClass('selected')
});