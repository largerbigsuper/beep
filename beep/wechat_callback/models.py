from django.db import models

from django_extensions.db.fields.json import JSONField

from utils.modelmanager import ModelManager

class WxBotManager(ModelManager):
    
    def update_bot(self, wxid, data):
        self.update_or_create(wxid=wxid, defaults=data)

class WxBot(models.Model):
    """wehub机器人
    {
        "action": "login",
        "appid": "2f04ba7a74d2a7be",
        "data": {
            "client_version": "0.4.14",
            "head_img": "http://wx.qlogo.cn/mmhead/ver_1/dGCJI2RADPbAicYOUXg9xOicBL4kugXFJ8DDA6E48TGgxAfibicKT28NR0cemdEJKbhLvWf52AdmDfBNflCOkAACzkWqvvgVaxk48CicjUgsliaII/132",
            "local_ip": "192.168.0.104",
            "machine_id": "dusk:11524",
            "nickname": "碗底有虫",
            "nonce": "aa22b7f56cbc49819a05fbb35eee2f73_wehub_1572241508",
            "wx_alias": "hulihutuEeee"
        },
        "wxid": "wxid_96r2lcupwp6f21"
    }
    """
    wxid = models.CharField(max_length=200, unique=True, verbose_name='wxid')
    wx_alias = models.CharField(max_length=200, blank=True, null=True, verbose_name='微信号')
    nickname = models.CharField(max_length=200, blank=True, null=True, verbose_name='微信昵称')
    head_img = models.CharField(max_length=200, blank=True, null=True, verbose_name='头像的url地址')
    nonce = models.CharField(max_length=200, blank=True, null=True, verbose_name='nonce')
    client_version = models.CharField(max_length=200, blank=True, null=True, verbose_name='client_version')
    machine_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='machine_id')
    local_ip = models.CharField(max_length=200, blank=True, null=True, verbose_name='local_ip')

    objects = WxBotManager()

    class Meta:
        db_table = 'wx_bot'


mm_WxBot = WxBot.objects


class WxUserManager(ModelManager):
    
    def update_user(self, bot_wxid, userinfo_dict):
        wxid = userinfo_dict.pop('wxid')
        self.update_or_create(bot_wxid=bot_wxid, wxid=wxid, defaults=userinfo_dict)

    def get_info(self, wxid):
        """获取用户信息
        """
        info = self.cache.get(wxid)
        if not info:
            wxuser = self.filter(wxid=wxid).first()
            if wxuser:
                info = {
                    'id': wxid,
                    'name': wxuser.nickname,
                    'avatar_url': wxuser.head_img,
                    'user_type': 'wechat'
                }
                self.cache.set(wxid, info)
            else:
                info = {}
        return info


class WxUser(models.Model):
    """微信用户
    - userInfo(好友信息结构)
    {
        "wxid":  "wxid",                //wxid
        "wx_alias": "xxxxx",            //微信号(有可能为空)
        "nickname":"xxxxx",             //微信昵称
        "remark_name" :"xxxx",          //好友备注
        "head_img":"http://xxxxxxxx"    //头像的url地址
        "sex" : xx ,    				//性别:1男，2女
        "country":"xxx",				//祖国(可能为空)
        "province":"xxxx",				//省份(可能为空)
        "city":"xxxxx"					//城市(可能为空)
    }
    //
    {
    "city": "Hangzhou",
    "country": "CN",
    "head_img": "http://wx.qlogo.cn/mmhead/ver_1/LLAfEupaibUHrwM3HbJSoXGh5C4ibNbESTKHrGkUfjfyHT0aGrJgZVoqGqrJUl6ZMJicR2jdMbsPices2Nus37icqSau6iaFYFRLIbic4KEqU8NXibI/132",
    "nickname": "Cvmars",
    "province": "Zhejiang",
    "remark_name": "贺小狗",
    "sex": 1,
    "wx_alias": "qq441849029",
    "wxid": "hehaifeng4235"
    }
    """
    wxid = models.CharField(max_length=200, verbose_name='wxid')
    wx_alias = models.CharField(max_length=200, blank=True, null=True, verbose_name='微信号')
    nickname = models.CharField(max_length=200, blank=True, null=True, verbose_name='微信昵称')
    remark_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='好友备注')
    head_img = models.CharField(max_length=200, blank=True, null=True, verbose_name='头像的url地址')
    sex = models.PositiveSmallIntegerField(default=1, verbose_name='性别:1男，2女')
    country = models.CharField(max_length=200, blank=True, null=True, verbose_name='祖国')
    province = models.CharField(max_length=200, blank=True, null=True, verbose_name='省份')
    city = models.CharField(max_length=200, blank=True, null=True, verbose_name='城市')
    bot_wxid = models.CharField(max_length=200, blank=True, null=True, verbose_name='bot_wxid')

    objects = WxUserManager()

    class Meta:
        db_table = 'wx_user'
        unique_together = [
            ['wxid', 'bot_wxid']
        ]
        


mm_WxUser = WxUser.objects


class WxGroupManager(ModelManager):
    
    def update_group(self, bot_wxid, groupinfo_dict):
        
        if 'room_wxid' in groupinfo_dict:
            wxid = groupinfo_dict['room_wxid']
        else:
            wxid = groupinfo_dict.pop('wxid')
        self.update_or_create(bot_wxid=bot_wxid, wxid=wxid, defaults=groupinfo_dict)


class WxGroup(models.Model):
    """[summary]
    - groupinfo(群信息结构):
    {
    "head_img": "http://wx.qlogo.cn/mmcrhead/uchmtWQh7iaqDiboEJT29lP9avibibicrDibuY5BDoI11mdwNd9GfrmTgsfib81K6bzu8wvoYKllShC0FK189Pfruymwib05m0FPkJeic/0",
    "member_count": 4,
    "member_nickname_list": [
        "Cvmars",
        "碗底有虫",
        "Zdz",
        "yu"
    ],
    "member_wxid_list": [
        "hehaifeng4235",
        "wxid_96r2lcupwp6f21",
        "wxid_smrapzzeruvp21",
        "wxid_r1nrc1u1m4qw22"
    ],
    "name": "先退的是狗",
    "owner_wxid": "hehaifeng4235",
    "room_wxid": "5609987290@chatroom",
    "wxid": "5609987290@chatroom"
    }
    """
    head_img = models.CharField(max_length=200, blank=True, null=True, verbose_name='头像的url地址')
    member_count = models.PositiveIntegerField(default=0, verbose_name='该群成员总数')
    member_nickname_list = JSONField(default='[]', verbose_name='成员昵称列表')
    member_wxid_list = JSONField(default='[]', verbose_name='当前群的成员wxid的列表')
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='群名称')
    owner_wxid = models.CharField(max_length=200, blank=True, null=True, verbose_name='群主wxid')
    room_wxid = models.CharField(max_length=200, blank=True, null=True, verbose_name='群wxid')
    wxid = models.CharField(max_length=200, verbose_name='wxid')
    bot_wxid = models.CharField(max_length=200, blank=True, null=True, verbose_name='bot_wxid')
    memberInfo_list = JSONField(default='[]', verbose_name='当前群的成员信息列表')

    objects = WxGroupManager()

    class Meta:
        db_table = 'wx_group'
        unique_together = [
            ['wxid', 'bot_wxid']
        ]


mm_WxGroup = WxGroup.objects


class WxMessageManager(ModelManager):
    pass

class WxMessage(models.Model):
    """[summary]
    - 文本消息
    {
        "msg_id": "xxxxx"             //消息id(字符串)
        "msg_timestamp": xxxxxx,      //消息的时间戳(单位为毫秒)
        "msg_type": 1,                      //1 代表文本消息
        "room_wxid": "xxxxxxxx@chatroom",   //聊天消息发生在哪个群(如果是私聊则为空)
        "wxid_from":  "wxid_xxxxxx",     	//消息发送者的wxid
                                            //如果是自己发的消息这里的wxid就是自己的微信号
        "wxid_to": 	"wxid_xxxxx",		 //消息的接收者的wxid
                                        //如果发往群的消息,这个值就是群的wxid
                                        //如果是别人私聊给自己的消息,这里就是自己的微信号
        "atUserList": ["xxx","xxx"]        //这条消息@的对象列表                       
        "msg": "xxxxxxxx"                //具体的文本内容
    //如果A在群里面at了B(群昵称为BN),C(群昵称为CN),则msg的格式为"@BN @CN XXXXXX" (@BN @CN之间有空格)
    }
      
    - 图片消息
    {
        "msg_id": "xxxxx",            //消息id(字符串)
        "msg_timestamp": xxxxxx,      //消息时间戳(单位为毫秒)
        "msg_type": 3, 					  //3 代表图片消息
        "room_wxid": "xxxxxxxx@chatroom", //同文本消息
        "wxid_from": "wxid_xxxxxx", 	//同文本消息
        "wxid_to": 	"wxid_xxxxx",		//同文本消息
        "file_index":"xxxxxx"   		//图片文件的唯一索引(由wehub生成)
        //该字段在wehub上报消息时有效
        //如果是自己发/转发的图片,file_index为本地的文件路径
    }
    - 链接消息(分享某个网页链接)
    {
        "msg_id": "xxxxx",            
        "msg_timestamp": xxxxxx,      
        "msg_type":49, 					//49 代表链接消息
        "room_wxid": "xxxxxxxx@chatroom", 
        "wxid_from": "wxid_xxxxxx", 
        "wxid_to": "wxid_xxxxxx", 
        "link_title":"标题", 			  //链接标题
        "link_desc": "副标题",           //链接描述（副标题）
        "link_url":"http://xxxxx", 		//分享链接的url
        "link_img_url": "http://xxxxxxx" //链接的缩略图的的Url,jpg或者png格式
        "raw_msg": "xxxxxxx"		//微信的原始消息,xml格式,0.3.14版本中新增
    }
    raw_msg 中的关键字段有"title","des","url","thumburl"(分别与link_title,link_desc,link_url,link_img_url值对应),如果link_url值为空,请自行分析raw_msg中的url.


    - 表情消息
    {
        "msg_id": "xxxxx",
        "msg_timestamp": xxxxxx,
        "msg_type":47, 					
        "room_wxid": "xxxxxxxx@chatroom", 
        "wxid_from": "wxid_xxxxxx", 
        "wxid_to": "wxid_xxxxxx", 
        "emoji_url": "xxxxxxxxx" //表情的url地址(若有需要,请回调接口自行下载该文件)
        "raw_msg": "xxxxxxx"  
    }
    - 小程序
    {
        "msg_id": "xxxxx",
        "msg_timestamp": xxxxxx,
        "msg_type":4901,
        "room_wxid": "xxxxxxxx@chatroom", 
        "wxid_from": "wxid_xxxxxx", 
        "wxid_to": "wxid_xxxxxx", 
        "raw_msg": "xxxxxxx"    //微信中的小程序信息的原始数据,xml格式,请自行解析
            //username,nickname 为关键字段
    }

    """

    msg_id = models.CharField(max_length=200, verbose_name='id')
    msg_timestamp = models.CharField(max_length=200, blank=True, null=True, verbose_name='时间戳')
    msg_type = models.CharField(max_length=200, blank=True, null=True, verbose_name='类型')
    room_wxid = models.CharField(max_length=200, blank=True, null=True, verbose_name='群wxid')
    wxid_from = models.CharField(max_length=200, blank=True, null=True, verbose_name='发送人')
    wxid_to = models.CharField(max_length=200, blank=True, null=True, verbose_name='接收人')
    atUserList = JSONField(default='[]', verbose_name='@用户列表')
    msg = models.CharField(max_length=2000, blank=True, null=True, verbose_name='文本内容')
    raw_msg = models.CharField(max_length=2000, blank=True, null=True, verbose_name='微信原始消息')
    
    file_index = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片文件索引')
    file_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片文件名')
    file_size = models.FloatField(default=0, verbose_name='文件大小')
    
    emoji_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='表情')

    link_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='标题')
    link_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='副标题')
    link_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='链接')
    link_img_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='链接所列图地址')
    bot_wxid = models.CharField(max_length=200, blank=True, null=True, verbose_name='bot_wxid')


    objects = WxMessageManager()

    class Meta:
        db_table = 'wx_message'

mm_WxMessage = WxMessage.objects

