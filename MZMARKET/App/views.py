from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustbuy, MainShop, MainShow, FoodType, Goods, MZUser
from App.views_config import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_OK
from App.views_helper import hash_str


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustbuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shows = MainShow.objects.all()

    data = {
        "title": '萌猪商城',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shop1_3': main_shop1_3,
        'main_shows': main_shows,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('mz:market_with_params', kwargs={
        'typeid': 104749,
        'childcid': 0,
        'order_rule': 0,
    }))


def market_with_params(request, typeid, childcid, order_rule):
    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)
    if childcid == ALL_TYPE:
        # 是0就显示全部,不进步一筛选
        pass
    else:
        # 不是0的话再继续查询childcid符合的商品
        goods_list = goods_list.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    print(typeid)
    foodtypes_childtypes = foodtypes.get(typeid=typeid).childtypenames.split('#')
    print(foodtypes_childtypes)
    for each_index, each_types in enumerate(foodtypes_childtypes):
        foodtypes_childtypes[each_index] = each_types.split(':')
    print(foodtypes_childtypes)

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'typeid': int(typeid),
        'foodtypes_childtypes': foodtypes_childtypes,
        'childcid': childcid,
        'order_rule_list': order_rule_list,
        'order_rule_params': order_rule,
    }
    return render(request, 'main/market.html', context=data)


def cart(request):
    return render(request, 'main/cart.html', context={'title': '萌猪购物车'})


def mine(request):
    return render(request, 'main/mine.html', context={'title': '萌猪个人中心'})


def register(request):
    if request.method == 'GET':
        data = {
            "title": "注册",
        }
        return render(request, 'user/register.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        icon = request.FILES.get('icon')
        password = hash_str(password)

        user = MZUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon
        user.u_roleid = len(role)

        user.save()

        return redirect(reverse('mz:login'))


def login(request):
    if request.method == "GET":
        return render(request, 'user/login.html', context={"title": '用户登录'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = hash_str(password)

        user = MZUser.objects.filter(u_username=username).filter(u_password=password).first()
        if user:
            return HttpResponse("登录成功：{}".format(user.u_roleid))
        else:
            return HttpResponse("用户名或密码不存在")


def check_user(request):
    username = request.GET.get('username')
    users = MZUser.objects.filter(u_username=username)

    data = {
        "status": HTTP_OK,
        "msg": 'username can be used',
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass
    return JsonResponse(data=data)