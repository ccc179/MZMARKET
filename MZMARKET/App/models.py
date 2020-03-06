from django.db import models

from App.views_config import ORDER_STATUS_NOT_PAY


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class MainWheel(Main):
    """
    insert into mzmarket_wheel(img,name,trackid) values
    """
    class Meta:
        db_table = 'mzmarket_wheel'


class MainNav(Main):
    """
    insert into mzmarket_nav(img,name,trackid)
    """
    class Meta:
        db_table = 'mzmarket_nav'


class MainMustbuy(Main):
    """
    insert into mzmarket_mustbuy(img,name,trackid)
    """
    class Meta:
        db_table = 'mzmarket_mustbuy'


class MainShop(Main):
    """
    insert into mzmarket_shop(img,name,trackid)
    """
    class Meta:
        db_table = 'mzmarket_shop'


class MainShow(Main):
    """
    insert into mzmarket_mainshow(trackid,name,img,categoryid,brandname,img1,childcid1,productid1,longname1,price1,
    marketprice1,img2,childcid2,productid2,longname2,price2,marketprice2,img3,childcid3,productid3,longname3,price3,
    marketprice3)
    """
    categoryid = models.IntegerField(default=1)
    brandname = models.CharField(max_length=64)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField(default=1)
    productid1 = models.IntegerField(default=1)
    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField(default=1)
    marketprice1 = models.FloatField(default=0)
    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=0)
    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=0)
    class Meta:
        db_table = 'mzmarket_mainshow'

    def __str__(self):
        return self.brandname


class FoodType(models.Model):
    """
    insert into mzmarket_foodtypes(typeid,typename,childtypenames,typesort)
    """
    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'mzmarket_foodtypes'

    def __str__(self):
        return self.typename


class Goods(models.Model):
    """
    insert into mzmarket_goods(productid,productimg,productname,productlongname,
    isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum)
    values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q",
    "","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);
    """
    productid = models.IntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=1)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'mzmarket_goods'

    def __str__(self):
        return self.productlongname


class MZUser(models.Model):
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to='icon/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    u_rolename = models.CharField(max_length=64, default="无")
    u_roleid = models.IntegerField(default=1)

    class Meta:
        db_table = 'mz_user'

    def __str__(self):
        return self.u_username


class Cart(models.Model):
    c_user = models.ForeignKey(MZUser)
    c_goods = models.ForeignKey(Goods)

    c_goods_num = models.IntegerField(default=1)
    c_is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'mzmarket_cart'

    def __str__(self):
        return self.c_user


class ServerInfo(models.Model):
    s_server_ip = models.CharField(max_length=32)
    s_server_port = models.CharField(max_length=32)
    s_server_username = models.CharField(max_length=32)
    s_server_password = models.CharField(max_length=64)

    def __str__(self):
        return self.s_server_ip


class Order(models.Model):
    o_user = models.ForeignKey(MZUser)
    o_paymoney = models.FloatField(default=0)
    o_create = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField(default=ORDER_STATUS_NOT_PAY)

    class Meta:
        db_table = 'mz_order'


class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order)
    o_goods = models.ForeignKey(Goods)
    o_goods_num = models.IntegerField(default=1)
    o_platformordernumber = models.CharField(max_length=255)
    o_extdata = models.CharField(max_length=128)
    o_realmoney = models.FloatField(default=0)

    class Meta:
        db_table = 'mz_ordergoods'