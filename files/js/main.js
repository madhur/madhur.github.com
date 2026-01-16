(function() {
    'use strict';

    // Parse query string
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

    document.addEventListener('DOMContentLoaded', function () {

        // Mobile navbar toggle (replacement for Bootstrap JS)
        var navbarToggle = document.querySelector('.navbar-toggle');
        var navbarCollapse = document.querySelector('.navbar-collapse');

        if (navbarToggle && navbarCollapse) {
            navbarToggle.addEventListener('click', function() {
                navbarCollapse.classList.toggle('in');
            });
        }

        // Highlight the project left navigation selected item
        if (document.URL.indexOf("projects") != -1) {
            var filename = document.URL.split('/').pop();
            var names = filename.split(".html");
            var basefile = decodeURIComponent(names[0].trim());

            document.querySelectorAll("div#projects ul li a").forEach(function (el) {
                var anchorText = el.textContent;
                if (basefile == anchorText) {
                    el.classList.add("active");
                }
            });
        }

        // Set up FancyBox
        if (typeof Fancybox !== 'undefined') {
            Fancybox.bind("[data-fancybox]", {});
        }

        // Set the responsive and normal search box values
        var qstring = qs["q"];
        if (qstring != null) {
            var q1 = document.getElementById("q1");
            var q2 = document.getElementById("q2");
            if (q1) q1.value = qstring;
            if (q2) q2.value = qstring;
        }

        // Load planes animation on special dates (Aug 15, Jan 26)
        var today = new Date();
        var month = today.getMonth() + 1;
        var day = today.getDate();
        if ((month === 8 && day === 15) || (month === 1 && day === 26)) {
            var script = document.createElement('script');
            script.src = '/files/js/vendor/planes.js';
            document.body.appendChild(script);
        }

    });

    // HTML encoding/decoding utilities
    function htmlEncode(value) {
        var div = document.createElement('div');
        div.textContent = value;
        return div.innerHTML;
    }

    function htmlDecode(value) {
        var div = document.createElement('div');
        div.innerHTML = value;
        return div.textContent;
    }

    // Print functionality
    window.Clickheretoprint = function() {
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
    };

})();
