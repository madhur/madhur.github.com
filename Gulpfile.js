const gulp = require('gulp');
const copy = require('gulp-copy');
const uglify = require('gulp-uglify');
const cssmin = require('gulp-cssmin');
const less = require('gulp-less');
const shell = require('gulp-shell');
const git = require('gulp-git');
const fs = require('fs');
const browserSync = require('browser-sync').create();

gulp.task('copy', function () {
    return gulp.src('files/css/styles.css')
        .pipe(copy('_site/files/css/', { prefix: 3 }));
});

gulp.task('uglify', function () {
    return gulp.src(['../site/files/js/app.js', '../site/files/js/main.js'])
        .pipe(uglify())
        .pipe(gulp.dest('../site/files/js/'));

});

gulp.task('cssmin', function () {
    return gulp.src([
        '../site/files/css/print.css',
        '../site/files/css/styles.css',
        '../site/files/css/searchresults.css',
        '../site/files/css/fancybox.css',
        '../site/files/css/syntax.css'
    ])
        .pipe(cssmin())
        .pipe(gulp.dest('../site/files/css/'));

});

gulp.task('build', shell.task([
    'jekyll build',
]));

gulp.task('less', function () {
    return gulp.src([
        'files/css/styles.less',
        'files/css/searchresults.less'
    ])
        .pipe(less())
        .pipe(gulp.dest('files/css/'));

});

gulp.task('reload', function (done) {
    browserSync.reload();
    done();
});

gulp.task('watch', function () {
    browserSync.init({
        ui: {
            port: 4001
        },
        port: 4000,
        server: {
            baseDir: '../site/'
        },
        open: true
    });

    gulp.watch('**', gulp.series('build', 'reload'));
});

gulp.task('gitadd', function () {
    //return git.add({ cwd: '../site/', quiet: false, });
    return gulp.src('../site/*')
        .pipe(git.add({ cwd: '../site/', quiet: false, }));
});

gulp.task('gitcommit', function () {
    let message = 'docs: Repository updated on ' + new Date().toISOString();
    return gulp.src('../site/*')
        .pipe(git.commit(message, {
            cwd: '../site/',
            quiet: false
        }));
});

gulp.task('gitpush', function (cb) {
    return git.push('origin', 'master', { cwd: '../site/', quiet: false }, function (err) {
        if (err) throw err;
        cb();
    });
});

gulp.task('nojekyll', function (cb) {
    fs.writeFile('../site/.nojekyll', '', cb);
});

gulp.task('git', gulp.series('gitadd', 'gitcommit', 'gitpush'));

gulp.task('lessCopy', gulp.series('less', 'copy'));

gulp.task('default', gulp.series('watch'));
gulp.task('deploy', gulp.series('build', 'uglify', 'cssmin', 'nojekyll'));
gulp.task('pushdeploy', gulp.series('build', 'uglify', 'cssmin', 'nojekyll', 'git'));
gulp.task('deploywithoutbuild', gulp.series('uglify', 'cssmin', 'nojekyll', 'git'));
