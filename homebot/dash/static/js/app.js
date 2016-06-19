var app = angular.module("app", ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: 'index.html'
        })
        .state('nextbus', {
            url: '/nextbus',
            templateUrl: '/partials/nextbus.html'
        })
});

app.controller("nextbus", function ($scope, $http,$interval) {

    $scope.refreshBus = function () {
        $http.get('/api/v1/nextbus').success(function (data) {
            $scope.data = data;
            $scope.busArrivals = [];
            angular.forEach(data, function (bus, index) {
                angular.forEach(bus.ArrivalTimes, function (arrivalTimes, index) {
                    $scope.busArrivals.push(arrivalTimes);
                });
            });
        })
    };
    $scope.refreshBus();
    $interval(function (){$scope.refreshBus();},120000);





});