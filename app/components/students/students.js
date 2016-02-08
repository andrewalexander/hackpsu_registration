'use strict';

app = angular.module('myApp.students', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/students', {
    templateUrl: 'components/students/students.html',
    controller: 'StudentsCtrl'
  });
}]);

app.factory('userFactory', ['$http', function($http) {

    var urlBase = 'http://:5000/api/';
    var userFactory = {};
    var config = { 
        headers: 
        {
            'Access-Control-Allow-Origin': 'True'
        }
    };

    userFactory.getUsers = function () {
        return $http.get(urlBase + 'users/', config);
    };
    userFactory.getUser = function (id) {
        return $http.get(urlBase + 'users/' + id , config);
    };
    userFactory.submitUser = function (user) {
        console.log('incoming user: '+ JSON.stringify(user))
        return $http.post(urlBase + 'submit', JSON.stringify(user), config);
    };
// return $resource('localhost:5000/users/:id', null,
//     {
//         'update': { method:'PUT' }
//     });
    return userFactory;
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('StudentsCtrl', ['$scope', '$routeParams', 'userFactory', '$http', function($scope, $routeParams, userFactory, $http) {
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
        var id = 123454321;
        var user = userFactory.getUser(id)
        .success(function (custs) {
            console.log('Got user ' + id + ' response: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            console.log('couldn\'t get user ' + id);
        });;
     
        userFactory.getUsers()
        .success(function (custs) {
            console.log('this: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            console.log('couldn\'t get all users');
        });
     
        userFactory.submitUser($scope.user)
        .success(function (custs) {
            console.log('this: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            console.log('couldn\'t submit user');
        });
    };
}]);