// Live search box built into the nav (layouts/partials/header.html), replacing
// the old "Search" nav item that linked out to /search/. Loaded on every page,
// but does nothing until the box is used: Fuse.js and the post index
// (index.json) are only fetched the first time the input is focused or typed
// into, so pages that never touch search pay no extra cost.
(function () {
    "use strict";

    var input = document.getElementById("navSearchInput");
    var form = document.getElementById("navSearchForm");
    var resultsList = document.getElementById("navSearchResults");
    if (!input || !form || !resultsList) {
        return;
    }

    var fuseOptions = {
        distance: 100,
        threshold: 0.4,
        ignoreLocation: true,
        keys: ["title", "permalink", "summary", "content"]
    };
    var RESULT_LIMIT = 8;

    var fuse = null;
    var loadPromise = null;
    var currentResults = [];
    var debounceTimer = null;

    function loadScript(src) {
        return new Promise(function (resolve, reject) {
            var script = document.createElement("script");
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    function ensureReady() {
        if (!loadPromise) {
            var fuseSrc = input.dataset.fuseSrc;
            var indexSrc = input.dataset.indexSrc;
            var scriptReady = window.Fuse ? Promise.resolve() : loadScript(fuseSrc);

            loadPromise = Promise.all([
                scriptReady,
                fetch(indexSrc).then(function (response) {
                    if (!response.ok) {
                        throw new Error("Search index load failed: " + response.status);
                    }
                    return response.json();
                })
            ]).then(function (parts) {
                fuse = new window.Fuse(parts[1], fuseOptions);
            }).catch(function (error) {
                loadPromise = null; // allow retry on next interaction
                console.error(error);
            });
        }
        return loadPromise;
    }

    function closeResults() {
        resultsList.hidden = true;
        resultsList.innerHTML = "";
        input.setAttribute("aria-expanded", "false");
        currentResults = [];
    }

    function renderResults(matches) {
        currentResults = matches;
        resultsList.innerHTML = "";

        if (!matches.length) {
            resultsList.hidden = true;
            input.setAttribute("aria-expanded", "false");
            return;
        }

        var fragment = document.createDocumentFragment();
        matches.forEach(function (match) {
            var li = document.createElement("li");
            li.setAttribute("role", "option");
            var a = document.createElement("a");
            a.className = "nav-search-result";
            a.href = match.item.permalink;
            a.textContent = match.item.title;
            li.appendChild(a);
            fragment.appendChild(li);
        });
        resultsList.appendChild(fragment);
        resultsList.hidden = false;
        input.setAttribute("aria-expanded", "true");
    }

    function runSearch() {
        var query = input.value.trim();
        if (!query) {
            closeResults();
            return;
        }
        if (!fuse) {
            return; // still loading; ensureReady() re-runs this once ready
        }
        renderResults(fuse.search(query, { limit: RESULT_LIMIT }));
    }

    input.addEventListener("focus", function () {
        ensureReady().then(runSearch);
    }, { once: true });

    input.addEventListener("input", function () {
        ensureReady();
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(runSearch, 150);
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (currentResults.length) {
            window.location.href = currentResults[0].item.permalink;
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            if (document.activeElement === input || form.contains(document.activeElement)) {
                input.value = "";
                closeResults();
                input.blur();
            }
            return;
        }

        if (!form.contains(document.activeElement)) {
            return;
        }

        var items = resultsList.querySelectorAll(".nav-search-result");
        if (!items.length) {
            return;
        }
        var active = document.activeElement;
        var index = Array.prototype.indexOf.call(items, active);

        if (event.key === "ArrowDown") {
            event.preventDefault();
            var next = index === -1 ? items[0] : items[index + 1];
            (next || items[0]).focus();
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            if (index <= 0) {
                input.focus();
            } else {
                items[index - 1].focus();
            }
        }
    });

    document.addEventListener("click", function (event) {
        if (!form.contains(event.target)) {
            closeResults();
        }
    });
})();
