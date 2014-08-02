require.config(
{
    baseUrl: '/files/js',
    paths:
    {
        // the left side is the module ID,
        // the right side is the path to
        // the jQuery file, relative to baseUrl.
        // Also, the path should NOT include
        // the '.js' file extension. This example
        // is using jQuery 1.9.0 located at
        // js/lib/jquery-1.9.0.js, relative to
        // the HTML page.
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

    },
    map:
    {
        'URI':
        {
            'IPv6': 'falsy',
            'punycode': 'falsy',
            'SecondLevelDomains': 'falsy'
        }
    }




});

require(["pace"]);


require(["main"]);