$(function () {
    var $username = $("#username_input");

    $username.change(function () {
        var username = $username.val().trim();

        if (username.length) {
            //   如果长度大于0 将用户名发送给服务器预校验
            $.getJSON('/mz/checkuser/', {"username": username}, function (data) {
                console.log(data);
                var $username_info = $("#username_info");
                if (data['status']===200){
                    $username_info.html("用户名可用").css("color",'green')
                }else if (data['status']===901){
                    $username_info.html("用户已存在").css('color','red')
                }
            });

        }

    });

})

function check() {
    var $username = $("#username_input");

    var username = $username.val().trim();
    if (!username){
        return false
    }

    var info_color = $("#username_info").css("color");
    console.log(info_color);
    if (info_color === 'rgb(255, 0, 0)'){
        return false
    }
    var $password_input = $("#password_input");
    var password = $password_input.val().trim();

    $password_input.val(md5(password));

    var $password_confirm_input = $("#password_confirm_input");
    var password_confirm = $password_confirm_input.val().trim();

    $password_confirm_input.val(md5(password_confirm));


    return true
}