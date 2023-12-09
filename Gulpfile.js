const gulp = require('gulp');
const connect = require('gulp-connect');
const copy = require('gulp-copy');
const uglify = require('gulp-uglify');
const cssmin = require('gulp-cssmin');
const less = require('gulp-less');
const shell = require('gulp-shell');
const git = require('gulp-git');
const fs = require('fs');
const browserSync = require('browser-sync').create();

gulp.task('connect', async function () {
    return connect.server({
        root: '../site/',
        port: 4000,
        livereload: true
    });
});

gulp.task('copy', function (cb) {
    gulp.src('files/css/styles.css')
        .pipe(copy('_site/files/css/', { prefix: 3 }));
    cb();
});

gulp.task('uglify', function (cb) {
    gulp.src(['../site/files/js/app.js', '../site/files/js/main.js'])
        .pipe(uglify())
        .pipe(gulp.dest('../site/files/js/'));

    cb();
});

gulp.task('cssmin', function (cb) {
    gulp.src([
        '../site/files/css/print.css',
        '../site/files/css/styles.css',
        '../site/files/css/searchresults.css',
        '../site/files/css/jquery.fancybox.css',
        '../site/files/css/syntax.css'
    ])
        .pipe(cssmin())
        .pipe(gulp.dest('../site/files/css/'));

    cb();
});

gulp.task('shell', shell.task([
    'jekyll build',
]));

gulp.task('less', function (cb) {
    return gulp.src([
        'files/css/styles.less',
        'files/css/searchresults.less'
    ])
        .pipe(less())
        .pipe(gulp.dest('files/css/'));

    cb();
});

gulp.task('watch', function (cb) {

    browserSync.init({
        server: {
            baseDir: '../site/'
        },
        open: true
    });
    gulp.task('watch', function () {
        gulp.watch('*.html', gulp.series('styles'));
        gulp.watch('layouts/*.*', gulp.series('scripts'));
        gulp.watch('_pages/*.*', gulp.series('images'));
    });
    cb();

});

gulp.task('gitadd', function (cb) {
    console.log("Adding to git")
    gulp.src('../site/*')
        .pipe(git.add({ cwd: '../site/' }));
    cb();
});

gulp.task('gitcommit', function (cb) {
    let message = 'docs: Repository updated on ' + new Date().toISOString();
    console.log(message)
    gulp.src('../site/*')
        .pipe(git.commit(message, {
            cwd: '../site/',
            disableMessageRequirement: true
        }));
    cb();
});

gulp.task('gitpush', function (cb) {
    console.log("Git push")
    git.push('origin', 'master', { cwd: '../site/' }, function (err) {
        if (err) throw err;
    });
    cb();
});

gulp.task('nojekyll', function (cb) {
    fs.writeFile('../site/.nojekyll', '', cb);
    cb();
});

//gulp.task('git', ['gitadd', 'gitcommit', 'gitpush']);
// gulp task to commit and push data on git
gulp.task('git', gulp.series('gitadd', 'gitcommit', 'gitpush'));

gulp.task('lessCopy', gulp.series('less', 'copy'));

gulp.task('default', gulp.series('connect', 'watch'));

gulp.task('jekyll', gulp.series('connect'));

gulp.task('deploy', gulp.series('shell', 'uglify', 'cssmin', 'nojekyll'));
gulp.task('pushdeploy', gulp.series('shell', 'uglify', 'cssmin', 'nojekyll', 'git'));
