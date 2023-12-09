const gulp = require('gulp');
const connect = require('gulp-connect');
const copy = require('gulp-copy');
const uglify = require('gulp-uglify');
const cssmin = require('gulp-cssmin');
const less = require('gulp-less');
const shell = require('gulp-shell');
const git = require('gulp-git');
const fs = require('fs');
const browserSync  = require('browser-sync').create();

gulp.task('connect', async function () {
    return connect.server({
        root: '../site/',
        port: 4000,
        livereload: true
    });
});

gulp.task('copy', async function () {
    return gulp.src('files/css/styles.css')
        .pipe(copy('_site/files/css/', { prefix: 3 }));
});

gulp.task('uglify', async function () {
    return gulp.src(['../site/files/js/app.js', '../site/files/js/main.js'])
        .pipe(uglify())
        .pipe(gulp.dest('../site/files/js/'));
});

gulp.task('cssmin', function () {
    return gulp.src([
        '../site/files/css/print.css',
        '../site/files/css/styles.css',
        '../site/files/css/searchresults.css',
        '../site/files/css/jquery.fancybox.css',
        '../site/files/css/syntax.css'
    ])
        .pipe(cssmin())
        .pipe(gulp.dest('../site/files/css/'));
});

gulp.task('shell', shell.task([
    'jekyll build',
    'jekyll serve'
]));

gulp.task('less', function () {
    return gulp.src([
        'files/css/styles.less',
        'files/css/searchresults.less'
    ])
        .pipe(less())
        .pipe(gulp.dest('files/css/'));
});

gulp.task('watch', async function() {

    browserSync.init({
        server: {
            baseDir: '../site/'
        },
        open: true
    });
    gulp.task('watch', function() {
        gulp.watch('*.html', gulp.series('styles'));
        gulp.watch('layouts/*.*', gulp.series('scripts'));
        gulp.watch('_pages/*.*', gulp.series('images'));
      });

   
});

gulp.task('gitadd', function () {
    return gulp.src('../site/**/*')
        .pipe(git.add({ args: '-A' }));
});

gulp.task('gitcommit', function () {
    let message = 'docs: Repository updated on ' + new Date().toISOString();
    return gulp.src('../site/**/*')
        .pipe(git.commit(message, {
            args: '-a',
            disableMessageRequirement: true
        }));
});

gulp.task('gitpush', function () {
    git.push('origin', 'master', { args: " ../site/" }, function (err) {
        if (err) throw err;
    });
});

gulp.task('nojekyll', async function (cb) {
    fs.writeFile('../site/.nojekyll', '', cb);
});

//gulp.task('git', ['gitadd', 'gitcommit', 'gitpush']);
// gulp task to commit and push data on git
gulp.task('git', function () {
    return gulp.series('gitadd', 'gitcommit', 'gitpush');
});
gulp.task('lessCopy', function () {
    return gulp.series('less', 'copy');
});
gulp.task('default', async function () {
    return gulp.series('connect', 'watch');
});
gulp.task('jekyll', function () {
    return gulp.series('connect');
});
gulp.task('deploy', function () {
    return gulp.series('shell', 'uglify', 'cssmin', 'nojekyll');
});
gulp.task('pushdeploy', function () {
    return gulp.series('shell', 'uglify', 'cssmin', 'nojekyll', 'git');
});
