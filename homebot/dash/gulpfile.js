var gulp = require('gulp');
var jshint = require('gulp-jshint');

gulp.task('lint', function () {
    gulp.src('./static/js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(jshint.reporter('fail'));
});

// gulp.task('copyangular', function(){
//     gulp.src('./static/bower_components/angular/angular.min.js')
//         .pipe(gulp.dest('./static/js'));
// });
//
// gulp.task('copybootstrap', function () {
//     gulp.src('./static/bower_components/bootstrap/dist/bootstrap.min.js')
//         .pipe(gulp.dest('./static/js'));
//     gulp.src('./static/bower_components/bootstrap/dist/bootstrap.min.css')
//         .pipe(gulp.dest('./static/css'));
// })

gulp.task('default', function () {
    // gulp.start('copyangular');
    // gulp.start('copybootstrap');
    gulp.start('lint')
});