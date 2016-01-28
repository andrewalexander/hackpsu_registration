'use strict';

app = angular.module('myApp.students', ['ngRoute', 'ngResource'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/students/:id', {
    templateUrl: 'components/students/students.html',
    controller: 'StudentsCtrl'
  });
}])

.controller('StudentsCtrl', ['$scope', '$resource',function($scope) { 
    $scope.master = {};

    // jsonify the scope.user -> send to back_end for jsonification and updating database
    $scope.update = function(user) {
        $scope.master = angular.copy(user);
    };

    $scope.reset = function() {
        $scope.user = angular.copy($scope.master);
    };

    $scope.reset();
}]);

app.factory('Users', ['$resource', function($resource) {
return $resource('http://54.210.83.129:5000/users/:id', null,
    {
        'update': { method:'PUT' }
    });
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('UsersCtrl', ['$scope', '$routeParams', 'Users', function($scope, $routeParams, Users) {
    $scope.send = function() {
        // First get a note object from the factory
        var user = Users.get({ id:$routeParams.id });
        var $id = user.id;

        // Now call update passing in the ID first then the object you are updating
        Users.update({ id:$id }, user);    
        // This will PUT /notes/ID with the note object in the request payload
    };
}]);