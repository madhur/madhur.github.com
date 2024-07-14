define(["jquery", "bootstrap", "fancybox"], function ($, bootstrap, fancybox) {

    var qs = (function (a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i) {
            var p = a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));




    $(document).ready(function () {
        // Animate fixed top navigation
        $(window).scroll(function () {
            if ($(".navbar").offset().top > 50) {
                $(".navbar-fixed-top").addClass("top-nav-collapse");
            }
            else {
                $(".navbar-fixed-top").removeClass("top-nav-collapse");
            }
        });



        // Highlight the project left navigation selected item
        var basefile;
        if (document.URL.indexOf("projects") != -1) {

            // var uri = new URI(document.URL);
            var filename = document.URL.split('/').pop();
            var names = filename.split(".html");

            basefile = names[0];
            basefile = decodeURIComponent(basefile.trim());

            $("div#projects ul li a").each(function () {
                var anchorText = $(this).text();
                if (basefile == anchorText)
                    $(this).addClass("active");
            });
        }

        // Set up fancy box
        fancybox.Fancybox.bind("[data-fancybox]", {
            // Your custom options
          });

        // Set the responsive and normal search box values
        var qstring = qs["q"];
        if (qstring != null) {
            $("#q1").val(qstring);
            $("#q2").val(qstring);
        }

        // Start carousel
        $('.carousel').carousel();

    });


    function htmlEncode(value) {
        return $('<div/>').text(value).html();
    }

    function htmlDecode(value) {
        return $('<div/>').html(value).text();
    }


    function Clickheretoprint() {
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



});