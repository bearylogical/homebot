var app = angular.module("app", ['ui.router'])  ;

app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: '/dash/partials/home.html'
        })
        .state('nextbus', {
            url: '/nextbus',
            templateUrl: '/dash/partials/nextbus.html'
        })
});

app.controller("nextbus", function ($scope, $http,$interval) {

    $scope.refreshBus = function () {
        $http.get('/api/v1/nextbus').success(function (data) {
            $scope.data = data;
            // $scope.busArrivals = [];
            // angular.forEach(data, function (bus, index) {
            //     angular.forEach(bus.ArrivalTimes, function (arrivalTimes, index) {
            //         $scope.busArrivals.push(arrivalTimes);
            //     });
            // });
        })
    };
    $scope.refreshBus();
    $interval(function (){$scope.refreshBus();},120000);
    
});

app.controller("home", function($scope,$http,$interval){

    $scope.getWeather = function () {
        $http.get('/api/v1/weather').success(function (WEAdata) {
            $scope.weather = WEAdata;
        })
    };

    $scope.getPSI = function () {
        $http.get('/api/v1/psi').success(function (PSIdata) {
            $scope.psi = PSIdata;
        })
    };

    $scope.greetingFunc = function (){
        var t = new Date();
        var hours = t.getHours();

        if (hours >=0 && hours <12){
            $scope.greeting = 'Morning';
        } else if (hours >= 12 && hours <= 17){
            $scope.greeting = 'Afternoon';
        } else{
            $scope.greeting = 'Evening';
        }
    };


    $scope.getTravel = function () {
        $http.get('/api/v1/transit').success(function (TRANSdata){
            $scope.transit = TRANSdata;
        })
    };

    $scope.greetingFunc();
    $scope.getTravel();
    $scope.getPSI();
    $scope.getWeather();
    $interval(function (){$scope.getPSI();},7200000);
});