$(document).ready(function () {
    $.get("/api", function (data) {
        console.log(typeof data); // string
        console.log(data); // HTML content of the jQuery.ajax page
        dat = JSON.parse(data);
        console.log(dat);
        $("#cookie").html(dat['cookie']);
    });
});