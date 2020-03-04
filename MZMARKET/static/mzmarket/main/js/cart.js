$(function () {
    // 我在这里点击勾选
    $(".confirm").click(function () {
        console.log('change state');
        var $confirm = $(this);
        var $li = $confirm.parents("li");
        var cartid = $li.attr("cartid");
        $.getJSON("/mz/changecartstate/", {"cartid": cartid}, function (data) {
            console.log(data);
            if (data["status"] === 200) {
                $("#total_price").html(data["total_price"]);
                if (data["c_is_select"]) {
                    $confirm.find("span").find("span").html("√");
                } else {
                    $confirm.find("span").find("span").html("");
                }
                if(data["is_all_select"]){
                    $(".all_select span span").html("√")
                }else {
                    $(".all_select span span").html("")
                }
            }
        })

    })
    // 我在这里点击减号
    $(".subShopping").click(function () {
        console.log("sub is clicked");
        var $sub = $(this);

        var $li = $sub.parents("li");

        var cartid = $li.attr("cartid");
        console.log(cartid);

        $.getJSON('/mz/subfromcart/', {"cartid": cartid}, function (data) {
            console.log(data);
            if (data["status"] === 200) {
                $("#total_price").html(data["total_price"]);
                if (data["c_goods_num"] > 0) {
                    $sub.next("span").html(data["c_goods_num"]);
                } else {
                    $li.remove();
                }
            }
        })
    });
//    我在这里点击加号
    $(".addShopping").click(function () {
        var $add = $(this);
        var $li = $add.parents("li");
        var goodsid = $li.attr("goodsid");
        $.getJSON('/mz/addtocart/', {"goodsid": goodsid},function (data) {
            console.log(data);
            $add.prev("span").html(data["c_goods_num"]);
            $("#total_price").html(data["total_price"]);
        })
    });
//    我在这里点击全选

//    ↑设置一下全选和非全选的列表
    $(".all_select").click(function () {
        var $all_select = $(this);
        var select_list = [];
        var unselect_list = [];
        $(".confirm").each(function () {
            var $confirm = $(this);
            var cartid = $confirm.parents("li").attr("cartid");
            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid)
            } else {
                unselect_list.push(cartid)
            }
        });
        if (unselect_list.length > 0) {
            console.log(unselect_list);
            $.getJSON("/mz/allselect/", {"cart_list": unselect_list.join("#")}, function (data) {
                console.log(data);
                if (data["status"] === 200) {
                    $("#total_price").html(data["total_price"]);
                    $(".confirm").find("span").find("span").html("√");
                    $all_select.find("span").find("span").html("√");
                }
            })
        } else {
            if (select_list.length > 0) {
                console.log(select_list);
                $.getJSON("/mz/allselect/", {"cart_list": select_list.join("#")}, function (data) {
                    console.log(data);
                    if (data["status"] === 200) {
                        $("#total_price").html(data["total_price"]);
                        $(".confirm").find("span").find("span").html("");
                        $all_select.find("span").find("span").html("");
                    }
                })
            }
        }
    })

})