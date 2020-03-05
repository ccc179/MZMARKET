import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustbuy, MainShop, MainShow, FoodType, Goods, MZUser, Cart
from App.views_config import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_OK
from App.views_helper import hash_str, sendemail_activate, get_total_price
from MZMARKET.settings import MEDIA_KEY_PREFIX


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
    # 如果用户是登录状态打开的本页面
    user_id = request.session.get("user_id")
    if user_id:
        cart_goods = Cart.objects.filter(c_user_id=user_id)
        if cart_goods.exists():
            data["cart_goods"] = cart_goods

    return render(request, 'main/market.html', context=data)


def cart(request):
    # 中间件实现了登录状态判断，request.user 是MZUser
    carts = Cart.objects.filter(c_user=request.user)

    is_all_select = not carts.filter(c_is_select=False).exists()

    data = {
        'title': '萌猪购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price(request.user),
    }
    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')
    data = {
        'title': '萌猪个人中心',
        'is_login': False,
    }

    if user_id:
        user = MZUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url

    return render(request, 'main/mine.html', context=data)


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
        password = make_password(password)

        user = MZUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon
        user.u_roleid = len(role)

        user.save()

        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60*60*24)
        print(u_token)
        sendemail_activate(username, email, u_token)

        return redirect(reverse('mz:login'))


def login(request):
    if request.method == "GET":
        notice = request.session.get("error_message")
        if notice:
            del request.session["error_message"]

            return render(request, 'user/login.html', context={"title": '用户登录', "error_message": notice})
        return render(request, 'user/login.html', context={"title": '用户登录'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = MZUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()
            if check_password(password, user.u_password):
                request.session['user_id'] = user.id
                return redirect(reverse('mz:mine'))
            else:
                request.session["error_message"] = "密码错误"
                print('密码错误')
                return redirect(reverse('mz:login'))
        print('用户名不存在')
        request.session["error_message"] = "用户名不存在"
        return redirect(reverse('mz:login'))


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


def log_out(request):
    request.session.flush()
    return redirect(reverse('mz:mine'))


def activate(request):
    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)

    if user_id:
        cache.delete("u_token")

        user = MZUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()

        return redirect(reverse('mz:login'))

    return render(request, 'user/activate_fail.html')


def add_to_cart(request):
    goodsid = request.GET.get("goodsid")
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user

    cart_obj.save()

    print(request.user)
    data = {
        'status': 200,
        'msg': 'ok',
        'c_goods_num': cart_obj.c_goods_num,
        'total_price': get_total_price(request.user),
    }
    return JsonResponse(data=data)


def change_cart_state(request):
    cart_id = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.c_is_select = not cart_obj.c_is_select
    cart_obj.save()

    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()
    data = {
        'status': 200,
        'msg': 'state changed',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price(request.user),
    }
    return JsonResponse(data=data)


def sub_from_cart(request):
    cart_id = request.GET.get("cartid")
    cart_obj = Cart.objects.get(pk=cart_id)

    data = {
        "status": 200,
        "msg": 'sub successed',

    }

    if cart_obj.c_goods_num >1:
        cart_obj.c_goods_num = cart_obj.c_goods_num-1
        cart_obj.save()
        data["c_goods_num"] = cart_obj.c_goods_num

    else:
        cart_obj.delete()
        data["c_goods_num"] = 0

    data['total_price'] = get_total_price(request.user)

    return JsonResponse(data=data)


def all_select(request):
    cart_list = request.GET.get("cart_list")
    print(cart_list)
    cart_list = cart_list.split("#")

    print(cart_list)

    carts = Cart.objects.filter(id__in=cart_list)
    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    data = {
        "status": 200,
        "msg": 'ok',
        'total_price': get_total_price(request.user),

    }
    return JsonResponse(data=data)


def sub_from_market(request):
    # 从market页面减，这里传回来的是goodsid
    goodsid = request.GET.get("goodsid")
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    data = {
        'status': 200,
        'msg': 'sub ok',
    }

    if carts.exists():
        cart_obj = carts.first()
        goodsNum = cart_obj.c_goods_num
        if goodsNum > 1:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            cart_obj.save()
            data['goodsNum'] = cart_obj.c_goods_num
        else:
            cart_obj.delete()
            data['goodsNum'] = 0
    return JsonResponse(data=data)