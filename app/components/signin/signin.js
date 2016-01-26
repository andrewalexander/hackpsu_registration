'use strict';

angular.module('myApp.signin', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/signin', {
    templateUrl: 'components/signin/signin.html',
    controller: 'SignInCtrl'
  });
}])

.controller('SignInCtrl', [function() {

}]);