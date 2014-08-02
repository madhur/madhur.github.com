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
                    "files/css/styles.css": "files/css/styles.less"
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

    grunt.registerTask('lessCopy', ['less:development', 'copy:css']);

    grunt.registerTask('default', ['connect:server',  'watch']);
};