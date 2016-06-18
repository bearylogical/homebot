var app = angular.module("app", ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: 'index.html'
        })
});

app.controller("nextbus", function ($scope, $http) {
    $http.get('/api/v1/nextbus').success(function (data) {
        $scope.data = data;
        $scope.busArrivals = [];
        angular.forEach(data, function (bus, index) {
            angular.forEach(bus.ArrivalTimes, function (arrivalTimes, index) {
                $scope.busArrivals.push(arrivalTimes);
            });
        });
    });
});