'use strict';

app = angular.module('myApp.admin', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/admin', {
    templateUrl: 'app/components/admin/admin.html',
    controller: 'AdminCtrl'
  });
}]);

app.factory('adminFactory', ['$http', function($http) {

    var urlBase = 'http://54.84.9.133:5000/api/';
    var adminFactory = {};
    var config = { 
        headers: 
        {
            'Access-Control-Allow-Origin': 'True'
        }
    };

    adminFactory.getUsers = function () {
        return $http.get(urlBase + 'users/', config);
    };
    adminFactory.getUser = function (id) {
        return $http.get(urlBase + 'users/' + id + '/', config);
    };
    adminFactory.submitUser = function (user) {
        console.log('incoming user: '+ JSON.stringify(user))
        return $http.post(urlBase + 'submit', JSON.stringify(user), config);
    };

    return adminFactory;
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('StudentsCtrl', ['$scope', '$routeParams', 'adminFactory', '$http', function($scope, $routeParams, adminFactory, $http) {
    $scope.master = {};

    // jsonify the scope.user -> send to back_end for jsonification and updating database
    $scope.update = function(user) {
        $scope.master = angular.copy(user);
    };

    $scope.reset = function() {
        $scope.user = angular.copy($scope.master);
    };

    $scope.reset();

    $scope.send = function() {
        // First get a note object from the factory
        var user = adminFactory.getUser(id)
        .success(function (custs) {
            console.log('Got user ' + id + ' response: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            console.log('couldn\'t get user ' + id);
        });;
     
        adminFactory.getUsers()
        .success(function (custs) {
            $scope.users = console.log('users: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            console.log('couldn\'t get all users: ' + JSON.stringify(error));
        });
     
        adminFactory.submitUser($scope.user)
        .success(function (custs) {
            console.log('this: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            console.log('Bad request: ' + JSON.stringify(error));
        });
    };
}]);