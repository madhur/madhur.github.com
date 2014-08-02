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

require(["pace"]);


require(["main"]);