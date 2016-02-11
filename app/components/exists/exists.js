'use strict';

app = angular.module('myApp.exists', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/exists/:action', {
    templateUrl: 'components/exists/exists.html',
    controller: 'ExistsCtrl'
  });
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('ExistsCtrl', ['$scope', '$routeParams', function($scope, $routeParams) {
    if ($routeParams.action =="rsvp") {
    	$scope.action = "RSVPed"
    } else {
    	$scope.action = $routeParams.action	
    }
    

}]);