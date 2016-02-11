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
    userFactory.submitUser = function (user) {
        // return $http.post(urlBase + 'submit', JSON.stringify(user), config);
        var postUrl = urlBase + 'submit';
        
        // POST it
        var res = $http({
            method: 'POST',
            url: postUrl,
            data: JSON.stringify(user),
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': 'True'
            }
          })
        console.log(res);
        return res
        };

    return userFactory;
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('StudentsCtrl', ['$location', '$scope', '$routeParams', 'userFactory', '$http', function($location, $scope, $routeParams, userFactory, $http) {
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

    $scope.send = function() {
        // console.log($scope.user.ethnicity.join(','));
        userFactory.submitUser($scope.user)
        .success(function (attendee) {
            console.log(attendee);
            if (attendee.message == 'user_exists') {
                $location.path('/exists/registered')
            } else {
                $location.path('/thanks/registering')
            }
        })
        .error(function (error) {
            alert(error);
            console.log('Bad request: ' + JSON.stringify(error));
        });
    };
}]);