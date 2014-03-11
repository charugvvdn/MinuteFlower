//  -----------------
//  Object prototypes
//  -----------------

RegExp.escape = function(text) {
  if (!arguments.callee.sRE) {
    var specials = ['/', '.', '*', '+', '?', '|', '(', ')', '[', ']', '{', '}', '\\'];
    arguments.callee.sRE = new RegExp('(\\' + specials.join('|\\') + ')', 'g');
  }
  return text.replace(arguments.callee.sRE, '\\$1');
}

String.prototype.replaceAll = function(search, replace) {
    return this.replace(new RegExp(RegExp.escape(search), 'g'), replace);
}

String.prototype.format = function() {
    var formatted = this;
    for (arg in arguments)
        formatted = formatted.replaceAll('{'+arg+'}', arguments[arg]);
    return formatted;
};

function sf(str, args) {
    for (arg in args)
        str = str.replaceAll('{'+arg+'}', args[arg]);
    return str;
}

//  -------------------------
//  General utility functions
//  -------------------------

function htmlEncode(value){
  return $('<div/>').text(value).html();
}

function htmlDecode(value){
  return $('<div/>').html(value).text();
}

function getCookie(name) {
    var arrCookies = document.cookie.split(";");
    for (var i in arrCookies)
    if (arrCookies[i].substr(0,arrCookies[i].indexOf("=")).replace(/^\s+|\s+$/g,"")==name)
        return unescape(arrCookies[i].substr(arrCookies[i].indexOf("=")+1));
}

function size(obj) {
    var len = obj.length ? --obj.length : 0;
    for (var k in obj) ++len;
    return len;
}

function idx(arr, key, def) {
    if (!arr) return def;
    if (key in arr)
        return arr[key];
    return def;
}

function uniqid(prepend) {
    if (prepend == undefined)
        prepend = "";
    return "" + prepend + uniqidCounter++;
}

function findId(arr, id) {
    for (var i in arr)
        if (parseInt(arr[i].id) == parseInt(id))
            return i;
    return -1;
}

function toUTC(date) {
    return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),  date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
}

function fromUTC(date) {
    return new Date(date.toUTCString());
}

function formatDate(date) {
   return dateFormat(date, 'd mmm h:MM TT');
}
