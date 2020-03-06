$(function () {
    $("#baoyuanpay").click(function () {
        console.log("go to top-up platform");
        var gameuser= $("#roleid").html().trim();
        var paymoney = $("#total_price").html().trim();
        var extdata = $("#orderid").html().trim();
        console.log(gameuser);
        console.log(paymoney);
        console.log(extdata);
        $.getJSON("http://pay.6799wan.com/Payment/Service/655a95acb9625f0c7fbd9d62973a07b2/?" +
            "gameuser="+gameuser+"&paymoney="+paymoney+"&extdata="+extdata,function (data) {
                console.log(data)
        })
    })
})