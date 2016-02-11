'use strict';

app = angular.module('myApp.rsvp', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/rsvp/:id', {
    templateUrl: 'components/rsvp/rsvp.html',
    controller: 'RsvpCtrl'
  });
}]);

app.factory('rsvpFactory', ['$http', function($http) {

    var urlBase = 'http://54.175.14.44:5000/api/';
    var rsvpFactory = {};
    var config = { 
        headers: 
        {
            'Access-Control-Allow-Origin': 'True'
        }
    };
    rsvpFactory.rsvp = function (rsvp) {
        return $http.post(urlBase + 'rsvp', JSON.stringify(rsvp), config);
    };

    return rsvpFactory;
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('RsvpCtrl', ['$scope', '$routeParams', 'rsvpFactory', '$http', function($scope, $routeParams, rsvpFactory, $http) {

    console.log($routeParams);
    
    $scope.send = function() {
        $scope.rsvp.user_id = $routeParams.id;
        console.log("RSVP:");
        console.log($scope.rsvp);
        rsvpFactory.rsvp($scope.rsvp)
        .success(function(resp){
            
            console.log(JSON.stringify(resp));
        })
        .error(function (error) {
            console.log('Bad request: ' + JSON.stringify(error));
        });
    };
    
}]);