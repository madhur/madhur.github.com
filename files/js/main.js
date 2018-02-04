define(["jquery", "bootstrap", "fancybox"], function($, bootstrap, fancybox)
{

    var qs = (function(a)
    {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p = a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));




    $(document).ready(function()
    {
        // Animate fixed top navigation
        $(window).scroll(function()
        {
            if ($(".navbar").offset().top > 50)
            {
                $(".navbar-fixed-top").addClass("top-nav-collapse");
            }
            else
            {
                $(".navbar-fixed-top").removeClass("top-nav-collapse");
            }
        });

     

        // Highlight the project left navigation selected item
        var basefile;
        if (document.URL.indexOf("projects") != -1)
        {

           // var uri = new URI(document.URL);
            var filename = document.URL.split('/').pop();
            var names = filename.split(".html");

            basefile = names[0];
            basefile = decodeURIComponent(basefile.trim());

            $("div#projects ul li a").each(function()
            {
                var anchorText = $(this).text();
                if (basefile == anchorText)
                    $(this).addClass("active");
            });
        }

        // Setup fancybox
        $("a").each(function()
        {
            if ($(this).has("img").length)
            {

                $(this).fancybox(
                {
                    padding: 0
                });

            }
        });

        // Set up fancy box
        $("a[href$='.jpg'],a[href$='.png'],a[href$='.gif']").attr('rel', 'gallery').fancybox(
        {
            padding: 0
        });


        // Expand accordion. Currently not used.
        // $(".accordion").click(function()
        // {

        //     $(this).next().slideToggle("normal");

        //     $(this).toggleClass("active");

        //     return false;

        // }).next().hide();


        // $("img", "#thumbs").hover(function()
        // {

        //     $(this).toggleClass("active");

        // }, function()
        // {

        //     $(this).toggleClass("active");

        // });


        // $("img", "#featured").hover(function()
        // {

        //     $(this).toggleClass("active");

        // }, function()
        // {

        //     $(this).toggleClass("active");

        // });


        // Set the responsive and normal search box values
        var qstring = qs["q"];
        if (qstring != null)
        {
            $("#q1").val(qstring);
            $("#q2").val(qstring);
        }

        // Start carousel
        $('.carousel').carousel();

    });


    function htmlEncode(value)
    {
        return $('<div/>').text(value).html();
    }

    function htmlDecode(value)
    {
        return $('<div/>').html(value).text();
    }


    function Clickheretoprint()
    {
        var docprint = window.open("", "", "");
        var sWinHTML = document.getElementById('blog-article').innerHTML;
        var heading = document.getElementsByTagName('h1')[0].innerHTML;
        docprint.document.open();
        docprint.document.write('<html><head><title>' + heading + '</title>');

        docprint.document.write('<link rel="stylesheet" type="text/css" href="/files/css/print.css">');
        docprint.document.write('</head><body onLoad="self.print()"><center>');
        docprint.document.write(sWinHTML);
        docprint.document.write('</center></body></html>');
        docprint.document.close();
        docprint.focus();
    }






    /*

// Hide Header on on scroll down
var didScroll;
var lastScrollTop = 0;
var delta = 5;
var navbarHeight = $('#navigation').outerHeight();


$(window).scroll(function(event) {
    didScroll = true;
});

setInterval(function() {
    if (didScroll) {
        hasScrolled();
        didScroll = false;
    }
}, 250);

function hasScrolled() {
    var st = $(this).scrollTop();

    // Make sure they scroll more than delta
    if (Math.abs(lastScrollTop - st) <= delta)
        return;

    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.

    if (findBootstrapEnvironment() == 'xs') {
        if (st > lastScrollTop && st > navbarHeight) {
            // Scroll Down
            $('#navigation').removeClass('nav-down').addClass('nav-up');
        } else {
            // Scroll Up
            if (st + $(window).height() < $(document).height()) {
                $('#navigation').removeClass('nav-up').addClass('nav-down');
            }
        }
    }

    lastScrollTop = st;
}

function findBootstrapEnvironment() {
    var envs = ['xs', 'sm', 'md', 'lg'];

    $el = $('<div>');
    $el.appendTo($('body'));

    for (var i = envs.length - 1; i >= 0; i--) {
        var env = envs[i];

        $el.addClass('hidden-' + env);
        if ($el.is(':hidden')) {
            $el.remove();
            return env
        }
    };
}*/

});