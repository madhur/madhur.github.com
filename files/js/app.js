require.config(
{
    baseUrl: '/files/js',
    paths:
    {      
        jquery: 'vendor/jquery',
        bootstrap: 'vendor/bootstrap.min',     
        fancybox: 'vendor/jquery.fancybox.pack',
        pace: 'vendor/pace.min',
        falsy: 'vendor/false.min',
        palnes: 'vendor/planes',
        main:'main'
    },
    shim:
    {
        "bootstrap":
        {

            deps: ["jquery"]
        },
        "fancybox":
        {
            deps: ["jquery"]
        }

    }
});

//require(["pace"]);


require(["main"]);

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0!
var yyyy = today.getFullYear();

if((dd ==15 && mm == 8) || (dd==26 && mm==1))
{
    require(["vendor/planes"], function()
    {
        doodle.init("/images/plane.png");

    });
}


