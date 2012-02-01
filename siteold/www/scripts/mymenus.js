//menu objects

function onLoad() {
    window.onResize = onLoad;
    loadMenus();
}

function loadMenus () {
    window.mySubMenu7 = new Menu("JavaScript");
    mySubMenu7.addMenuItem("JavaScript 1.0", "top.window.location='http://developer.netscape.com'");
    mySubMenu7.addMenuItem("JavaScript 1.1", "top.window.location='http://developer.netscape.com'");
    mySubMenu7.addMenuItem("JavaScript 1.2", "top.window.location='http://developer.netscape.com'");
    mySubMenu7.menuHiliteBgColor = "pink";

    window.myMenu7 = new Menu("Technologies");
    myMenu7.addMenuItem("Dynamic HTML", "top.window.location='http://developer.netscape.com'");
    myMenu7.addMenuItem("Java", "top.window.location='http://home.netscape.com'");
    myMenu7.addMenuItem("Plug-ins", "top.window.location='http://home.netscape.com'");

    window.myMenu3 = new Menu("Colors");
    myMenu3.addMenuItem("Red", "top.window.frames[1].document.bgColor='red'");
    myMenu3.addMenuItem("Green", "top.window.frames[1].document.bgColor='green'");
    myMenu3.addMenuItem("Blue", "top.window.frames[1].document.bgColor='blue'");
    myMenu3.addMenuItem("White", "top.window.frames[1].document.bgColor='white'");
    myMenu3.menuHiliteBgColor = "#6699CC";

    window.mozilla = new Menu("Mozilla");
    mozilla.addMenuItem("Mozilla.org", "top.window.frames[1].location='http://www.mozilla.org'");
    mozilla.addMenuItem("Projects", "http://www.mozilla.org/projects.html'");
    mozilla.addMenuItem("Source Code", "top.window.frames[1].location='http://www.mozilla.org/source-code.html'");
    mozilla.menuHiliteBgColor = "red";

	mozilla.writeMenus();
}
