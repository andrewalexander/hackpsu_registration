'use strict';

app = angular.module('myApp.students', ['ngRoute', 'checklist-model'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/students', {
    templateUrl: 'components/students/students.html',
    controller: 'StudentsCtrl'
  });
}]);

app.factory('userFactory', ['$http', function($http) {

    var urlBase = 'http://52.90.183.200:5000/api/';
    var userFactory = {};
    var config = { 
        headers: 
        {
            'Access-Control-Allow-Origin': 'True'
        }
    };

    // userFactory.getUsers = function () {
    //     return $http.get(urlBase + 'users/', config);
    // };
    // userFactory.getUser = function (id) {
    //     return $http.get(urlBase + 'users/' + id + '/', config);
    // };
    userFactory.submitUser = function (user) {
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
    $scope.ethnicity_choices = {
        opt_out: 'I prefer not to answer',
        asian: 'Asian',
        black: 'Black',
        filipino: 'Filipino',
        hawaiian: 'Hawaiian',
        hispanic: 'Hispanic',
        other: 'Other/Unknown',
        white: 'White/Caucasion'
    };
    $scope.dietary_choices = {
        vegan: 'Vegan',
        vegetarian: 'Vegetarian',
        pescetarian: 'Pescetarian',
        allergy_peanut: 'Peanut Allergy',
        allergy_lactose: 'Dairy Allergy/Lactose Intolerant',
        allergy_egg: 'Egg Allergy',
        allergy_gluen: 'Gluten Allergy',
        kosher: 'Kosher',
        halal: 'Halal'
    };

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
        console.log($scope.user);
        // console.log($scope.user.ethnicity.join(','));
        userFactory.submitUser($scope.user)
        .success(function (custs) {
            console.log('this: ' + JSON.stringify(custs));
        })
        .error(function (error) {
            alert(error);
            console.log('Bad request: ' + JSON.stringify(error));
        });
    };
}]);