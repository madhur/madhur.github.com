// Gruntfile.js
module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        connect: {
            server: {
                options: {
                    port: 4000,
                    base: '../site/',
                    livereload: true,
                    app: '/opt/google/chrome/chrome'

                }
            },
            server1: {
                options: {
                    port: 4000,
                    base: '../site/',
                    keepalive: true,
                    app: '/opt/google/chrome/chrome'

                }
            }

        },



        copy: {
            css: {
                files: {
                    '_site/files/css/styles.css': 'files/css/styles.css'
                }
            }
        },

        uglify: {
            options: {
                mangle: false
            },
            js: {
                files: {
                    '../site/files/js/app.js': ['../site/files/js/app.js'],
                    '../site/files/js/main.js': ['../site/files/js/main.js']
                }
            }
        },

        cssmin: {
            add_banner: {
                options: {
                    banner: '/* Minification done by Madhur Ahuja */'
                },
                files: {
                    '../site/files/css/print.css': ['../site/files/css/print.css'],
                    '../site/files/css/styles.css': ['../site/files/css/styles.css'],
                    '../site/files/css/searchresults.css': ['../site/files/css/searchresults.css'],
                    '../site/files/css/jquery.fancybox.css': ['../site/files/css/jquery.fancybox.css'],
                    '../site/files/css/syntax.css': ['../site/files/css/syntax.css'],
                }
            }
        },

        shell: {
            jekyllBuild: {
                command: 'jekyll build'
            },
            jekyllServe: {
                command: 'jekyll serve'
            }
        },

        less: {
            development: {
                options: {
                    paths: ["files/css/"]
                },
                files: {
                    "files/css/styles.css": "files/css/styles.less",
                    "files/css/searchresults.css": "files/css/searchresults.less",
                }
            }
        },

        watch: {

            less: {
                // Using less to render styles.
                // Watch for the *.less file sonly
                files: ['files/css/*.less', '*'],
                tasks: ['less', 'lessCopy']
            },

            jekyll: {

                files: [

                    '_includes/*.html',
                    '_layouts/*.html',
                    '_posts/*.markdown',
                    '_config.yml',
                    '**/*.markdown',
                    '**/*.md',
                    '_data/*/*.yaml',
                    '_data/*/*.yml',
                    '!_site/*.*'

                ],
                tasks: ['shell:jekyllBuild'],
                options: {
                    interrupt: true,
                    atBegin: true
                }
            },

        },


        // git add -A
        gitadd: {
            task: {
                options: {
                    force: true,
                    all: true,
                    cwd: '../site/'
                }
            }
        },

        // git commit -m "Repository updated on <current date time>"
        gitcommit: {
            task: {
                options: {
                    message: 'docs: Repository updated on ' + grunt.template.today(),
                    allowEmpty: true,
                    cwd: '../site/'
                }
            }
        },

        // git push origin master
        gitpush: {
            task: {
                options: {
                    remote: 'origin',
                    branch: 'master',
                    cwd: '../site/'
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
    grunt.loadNpmTasks('grunt-git');

    grunt.registerTask('nojekyll', 'Creates an empty file', function() {
        grunt.file.write('../site/.nojekyll', '');
    });


    // Create task
    grunt.registerTask('git', [
        'gitadd',
        'gitcommit:task',
        'gitpush:task'
    ]);

    grunt.registerTask('lessCopy', ['less:development', 'copy:css']);

    grunt.registerTask('default', ['connect:server', 'watch']);
    grunt.registerTask('jekyll', ['connect:server1']);
    grunt.registerTask('deploy', ['shell:jekyllBuild', 'uglify:js', 'cssmin', 'nojekyll']);
    grunt.registerTask('pushdeploy', ['shell:jekyllBuild', 'uglify:js', 'cssmin', 'nojekyll', 'git']);
};
