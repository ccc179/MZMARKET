$(function () {
    $("#all_types").click(function () {
        console.log("我被点击了");
        var $all_types_container = $("#all_types_container");
        $all_types_container.show();

        var $all_type = $(this);
        var $span = $all_type.find("span").find("span");
        $span.removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");

        var $all_sort_container = $("#all_sort_container");
        $all_sort_container.hide();

        var $all_sort = $("#all_sort");
        var $span_sort = $all_sort.find("span").find("span");
        $span_sort.removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
    });

    $("#all_types_container").click(function () {
        var $all_type_container = $(this);
        $all_type_container.hide();

        var $all_type = $("#all_types");
        var $span = $all_type.find("span").find("span");
        $span.removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down")


    });

    // 这里定义点击排序的动作，首次点击展开
    $("#all_sort").click(function () {
        console.log("排序也被点击了");
        var $all_sort_container = $("#all_sort_container");
        $all_sort_container.show();

    // 点击后下箭头变成上箭头
        var $all_sort = $(this);
        var $span = $all_sort.find("span").find("span");
        $span.removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");

        var $all_type_container = $("#all_types_container");
        $all_type_container.hide();

        var $all_type = $("#all_types");
        var $span_type = $all_type.find("span").find("span");
        $span_type.removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");

    });
    // 点击模块隐藏
    $("#all_sort_container").click(function () {
        var $all_sort_container = $(this);
        $all_sort_container.hide();

        var $all_sort = $("#all_sort");
        var $span = $all_sort.find("span").find("span");
        $span.removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down")
    });


});