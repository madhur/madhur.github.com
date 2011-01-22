//API for Menu Component 0.7 980802

function MenuAPI(o) {
	o.setFontSize = setFontSize;
	o.setFontWeight = setFontWeight;
	o.setFontFamily = setFontFamily;
	o.setFontColor = setFontColor;
	o.setFontColorHilite = setFontColorHilite;
	o.setBgColor = setBgColor;
	o.setMenuBorder = setMenuBorder;
	o.setMenuItemBorder = setMenuItemBorder;
	o.setMenuItemIndent = setMenuItemIndent;
	o.setMenuItemHeight = setMenuItemHeight;
	o.setMenuItemBgColor = setMenuItemBgColor;
	o.setMenuLiteBgColor = setMenuLiteBgColor;
	o.setMenuBorderBgColor = setMenuBorderBgColor;
	o.setMenuHiliteBgColor = setMenuHiliteBgColor;
	o.setMenuContainerBgColor = setMenuContainerBgColor;
	o.setChildMenuIcon = setChildMenuIcon;
	o.setChildMenuIconHilite = setChildMenuIconHilite;
	o.setMenuTransparency = setMenuTransparency;
}

function setFontSize(size) {
	this.fontSize = size;
}
function setFontWeight(weight) {
	this.fontWeight = weight;
}
function setFontFamily(family) {
	this.fontFamily = family;
}
function setFontColor(color) {
	this.fontColor = color;
}
function setFontColorHilite(color) {
	this.fontColorHilite = color;
}
function setBgColor(color) {
	this.bgColor = color;
}
function setMenuBorder(border) {
	this.menuBorder = border;
}
function setMenuItemBorder(border) {
	this.menuItemBorder = border;
}
function setMenuItemIndent(indent) {
	this.menuItemIndent = indent;
}
function setMenuItemHeight(height) {
	this.menuItemHeight = height;
}
function setMenuItemWidth(width) {
	this.menuWidth = width;
}
function setMenuLiteBgColor(color) {
	this.menuLiteBgColor = color;
}
function setMenuItemBgColor(color) {
	this.menuItemBgColor = color;
}
function setMenuBorderBgColor(color) {
	this.menuBorderBgColor = color;
}
function setMenuHiliteBgColor(color) {
	this.menuHiliteBgColor = color;
}
function setMenuContainerBgColor(color) {
	this.menuContainerBgColor = color;
}
function setChildMenuIcon(url) {
	this.childMenuIcon = url;
}
function setChildMenuIconHilite() {
	this.childMenuIconHilite = url;
}
function setMenuTransparency() {
    this.setMenuContainerBgColor(null);
    this.setMenuLiteBgColor(null);
	this.setBgColor(null);
    this.setMenuBorderBgColor(null);
    this.setMenuItemBgColor(null);
}