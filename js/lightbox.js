// Lightweight, dependency-free replacement for the old Jekyll site's Fancybox
// integration. Several posts already carry `<a href="img.png" data-fancybox>`
// markup (written for Fancybox, which never made it into the Hugo migration —
// those links just plain-navigated to the raw image until this script), and
// the /projects/ screenshot gallery (layouts/partials/extend_post_content.html)
// uses the same attribute. No markup changes needed for the existing posts.
//
// Grouping: elements are grouped by their data-fancybox attribute's exact
// value, including the empty string — so a post with several bare
// `data-fancybox` images (no value) becomes one prev/next-able gallery on that
// page, matching classic Fancybox's default behavior for that markup pattern.
(function () {
    "use strict";

    var links = Array.prototype.slice.call(document.querySelectorAll("[data-fancybox]"));
    if (!links.length) {
        return;
    }

    var groups = {};
    links.forEach(function (a) {
        var key = a.getAttribute("data-fancybox") || "";
        (groups[key] = groups[key] || []).push(a);
    });

    var overlay, imgEl, closeBtn, prevBtn, nextBtn;
    var currentGroup = [];
    var currentIndex = 0;

    function build() {
        overlay = document.createElement("div");
        overlay.className = "lightbox-overlay";
        overlay.setAttribute("role", "dialog");
        overlay.setAttribute("aria-modal", "true");
        overlay.setAttribute("aria-label", "Image viewer");
        overlay.hidden = true;

        imgEl = document.createElement("img");
        imgEl.className = "lightbox-img";

        closeBtn = document.createElement("button");
        closeBtn.type = "button";
        closeBtn.className = "lightbox-close";
        closeBtn.setAttribute("aria-label", "Close");
        closeBtn.textContent = "×";

        prevBtn = document.createElement("button");
        prevBtn.type = "button";
        prevBtn.className = "lightbox-nav lightbox-prev";
        prevBtn.setAttribute("aria-label", "Previous image");
        prevBtn.textContent = "‹";

        nextBtn = document.createElement("button");
        nextBtn.type = "button";
        nextBtn.className = "lightbox-nav lightbox-next";
        nextBtn.setAttribute("aria-label", "Next image");
        nextBtn.textContent = "›";

        overlay.appendChild(closeBtn);
        overlay.appendChild(prevBtn);
        overlay.appendChild(imgEl);
        overlay.appendChild(nextBtn);
        document.body.appendChild(overlay);

        closeBtn.addEventListener("click", close);
        prevBtn.addEventListener("click", function () { show(currentIndex - 1); });
        nextBtn.addEventListener("click", function () { show(currentIndex + 1); });
        overlay.addEventListener("click", function (event) {
            if (event.target === overlay) {
                close();
            }
        });
        document.addEventListener("keydown", function (event) {
            if (overlay.hidden) {
                return;
            }
            if (event.key === "Escape") {
                close();
            } else if (event.key === "ArrowLeft") {
                show(currentIndex - 1);
            } else if (event.key === "ArrowRight") {
                show(currentIndex + 1);
            }
        });
    }

    function show(index) {
        var len = currentGroup.length;
        currentIndex = (index + len) % len;
        imgEl.src = currentGroup[currentIndex].getAttribute("href");
        var multi = len > 1;
        prevBtn.hidden = !multi;
        nextBtn.hidden = !multi;
    }

    function open(group, index) {
        currentGroup = group;
        if (!overlay) {
            build();
        }
        overlay.hidden = false;
        document.body.classList.add("lightbox-open");
        show(index);
        closeBtn.focus();
    }

    function close() {
        overlay.hidden = true;
        document.body.classList.remove("lightbox-open");
        imgEl.src = "";
    }

    Object.keys(groups).forEach(function (key) {
        var group = groups[key];
        group.forEach(function (a, i) {
            a.addEventListener("click", function (event) {
                event.preventDefault();
                open(group, i);
            });
        });
    });
})();
