// Gruntfile.js
module.exports = function(grunt)
{
    grunt.initConfig(
    {
        pkg: grunt.file.readJSON('package.json'),

        connect:
        {
            server:
            {
                options:
                {
                    port: 4000,
                    base: './_site/',
                    livereload: true,
                    open: 'http://localhost:4000'

                }
            },
             server1:
            {
                options:
                {
                    port: 4000,
                    base: './_site/',
                    keepalive: true,
                    open: 'http://localhost:4000'

                }
            }

        },



        copy:
        {
            css:
            {
                files:
                {
                    '_site/files/css/styles.css': 'files/css/styles.css'
                }
            }
        },

        uglify:
        {
            options:
            {
                mangle: false
            },
            js:
            {
                files:
                {
                    '_site/files/js/app.js': ['_site/files/js/app.js'],
                    '_site/files/js/main.js': ['_site/files/js/main.js']
                }
            }
        },

        cssmin:
        {
            add_banner:
            {
                options:
                {
                    banner: '/* Minification done by Madhur Ahuja */'
                },
                files:
                {
                    '_site/files/css/print.css': ['_site/files/css/print.css'],
                    '_site/files/css/styles.css': ['_site/files/css/styles.css'],
                    '_site/files/css/searchresults.css': ['_site/files/css/searchresults.css'],
                    '_site/files/css/jquery.fancybox.css': ['_site/files/css/jquery.fancybox.css'],
                    '_site/files/css/syntax.css': ['_site/files/css/syntax.css'],
                }
            }
        },

        shell:
        {
            jekyllBuild:
            {
                command: 'jekyll build'
            },
            jekyllServe:
            {
                command: 'jekyll serve'
            }
        },

        less:
        {
            development:
            {
                options:
                {
                    paths: ["files/css/"]
                },
                files:
                {
                    "files/css/styles.css": "files/css/styles.less",
                    "files/css/searchresults.css": "files/css/searchresults.less",
                }
            }
        },

        watch:
        {

            less:
            {
                // Using less to render styles.
                // Watch for the *.less file sonly
                files: ['files/css/*.less'],
                tasks: ['less', 'lessCopy']
            },

            jekyll:
            {

                files: [
                    '_includes/*.html',
                    '_layouts/*.html',
                    '_posts/*.markdown',
                    '_config.yml',
                    '*.markdown'
                ],
                tasks: ['shell:jekyllBuild'],
                options:
                {
                    interrupt: true,
                    atBegin: true
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');


    grunt.registerTask('lessCopy', ['less:development', 'copy:css']);

    grunt.registerTask('default', ['connect:server', 'watch']);
    grunt.registerTask('jekyll', ['connect:server1']);
    grunt.registerTask('deploy', ['shell:jekyllBuild', 'uglify:js', 'cssmin']);
};