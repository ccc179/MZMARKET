import hashlib

from django.core.mail import send_mail
from django.template import loader

from App.models import Cart
from MZMARKET.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


def sendemail_activate(username, reveive, u_token):
    data = {
        "username": username,
        "activate_url": 'http://{}:{}/mz/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)
    }

    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(
        subject='萌猪邮箱激活%s' % username,
        message='neirong',
        html_message=html_message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[reveive, ],
        fail_silently=False,

    )


def get_total_price(user):
    '''
    :param allcarts:传进来的是符合当前用户request.user：
        需要进一步筛选c_is_select的结果用于计算
    :return:
        所有选中的商品的数量*价格
    '''
    carts = Cart.objects.filter(c_user=user).filter(c_is_select=True)

    total = 0
    for cart in carts:
        total += cart.c_goods_num * cart.c_goods.price
    return total
