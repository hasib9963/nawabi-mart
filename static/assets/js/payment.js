$(document).ready(function () {
    // Menu Toggle Script
    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    // Bootstrap tab switching
    $('a[data-toggle="tab"]').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});
