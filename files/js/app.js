require.config(
{
    baseUrl: '/files/js',
    paths:
    {      
        jquery: 'vendor/jquery',
        bootstrap: 'vendor/bootstrap.min',     
        pace: 'vendor/pace.min',
        falsy: 'vendor/false.min',
        palnes: 'vendor/planes',
        fancybox: 'vendor/fancybox.umd',
        typeahead: 'vendor/typeahead.min',
        bloodhound: 'vendor/bloodhound.min',
        main:'main'
    },
    shim:
    {
        "bootstrap":
        {

            deps: ["jquery"]
        },
        typeahead: {
            deps: [ 'jquery' ],
            init: function ($) {
                return require.s.contexts._.registry['typeahead.js'].factory( $ );
            }
        },
        bloodhound: {
            deps: ['jquery'],
            exports: 'Bloodhound'
         }

    }
});

//require(["pace"]);


require(["main"]);

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0!

if((dd ==15 && mm == 8) || (dd==26 && mm==1))
{
    require(["vendor/planes"], function()
    {
        doodle.init("/images/plane.png");

    });
}





