'use strict';

app = angular.module('myApp.admin', ['ngRoute', 'checklist-model'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/admin', {
    templateUrl: 'app/components/admin/admin.html',
    controller: 'AdminCtrl'
  });
}]);

app.factory('adminFactory', ['$http', function($http) {

    // var urlBase = 'http://52.90.183.200:5000/api/';
    var urlBase = 'http://localhost:5000/api/';
    var adminFactory = {};
    var config = { 
        headers: 
        {
            'Access-Control-Allow-Origin': 'True'
        }
    };

    adminFactory.getAllAttendees = function () {
        return $http.get(urlBase + 'users/', config);
    };
    adminFactory.sendEmail = function (email) {
        return $http.post(urlBase + 'send_email', JSON.stringify(email), config);
    };
    // adminFactory.getUser = function (id) {
    //     return $http.get(urlBase + 'users/' + id + '/', config);
    // };
    // adminFactory.submitUser = function (user) {
    //     console.log('incoming user: '+ JSON.stringify(user))
    //     return $http.post(urlBase + 'submit', JSON.stringify(user), config);
    // };

    return adminFactory;
}]);

// In our controller we get the ID from the URL using ngRoute and $routeParams
// We pass in $routeParams and our Notes factory along with $scope
app.controller('AdminCtrl', ['$scope', '$routeParams', 'adminFactory', '$http', function($scope, $routeParams, adminFactory, $http) {
    $scope.master = {};

    // // jsonify the scope.user -> send to back_end for jsonification and updating database
    // $scope.update = function(user) {
    //     $scope.master = angular.copy(user);
    // };

    // $scope.reset = function() {
    //     $scope.user = angular.copy($scope.master);
    // };

    // $scope.reset();

    $scope.get_attendees = function() {
        var attendees = adminFactory.getAllAttendees()
        .success(function (attendees) {
            $scope.attendee_emails = []
            var attendees_from_db = attendees.response
            for (var i = 0; i < attendees_from_db.length; i++) { 
                $scope.attendee_emails += String(attendees_from_db[i].email) + ',\n';
            }
            console.log(JSON.stringify($scope.attendee_emails))
            // console.log('Got attendees' + JSON.stringify(attendees));
        })
        .error(function (error) {
            console.log('Server Error: ' + error);
        });
    }

    $scope.send = function() {
        // First get a note object from the factory
        

        // var full_email = $scope.email.from_address + '@hackpsu.org';
        var request_data = angular.copy($scope.email)
        request_data.from_address = request_data.from_address + '@hackpsu.org'
        console.log($scope.email);
        adminFactory.sendEmail(request_data)
        .success(function (response) {
            $scope.emails_from_db = response.attendees;
            console.log('Got response' + JSON.stringify(response));
            $scope.reset();
        })
        .error(function (error) {
            console.log('Server Error: ' + error);
        });
     
        // adminFactory.getUsers()
        // .success(function (custs) {
        //     $scope.users = console.log('users: ' + JSON.stringify(custs));
        // })
        // .error(function (error) {
        //     console.log('couldn\'t get all users: ' + JSON.stringify(error));
        // });
     
        // adminFactory.submitUser($scope.user)
        // .success(function (custs) {
        //     console.log('this: ' + JSON.stringify(custs));
        // })
        // .error(function (error) {
        //     console.log('Bad request: ' + JSON.stringify(error));
        // });
    };
}]);