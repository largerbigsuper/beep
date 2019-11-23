from celery import shared_task


from utils.wexin_api import WeiXinData, WeiXinSubscribeMessageApi
from .models import mm_WxSubMessage, mm_WxSubscription

@shared_task
def send_activity_start_notice(pk):
    """微信订阅消息--活动开始
    """

    obj = mm_WxSubMessage.filter(pk=pk).first()
    if not obj:
        return
    if obj.wx_template.name == mm_WxSubMessage.activity_dict['name']:
        # 发送活动推送
        openid_list = list(mm_WxSubscription.filter(wx_template=obj.wx_template).values_list('user__mini_openid', flat=True))
        template_id = obj.wx_template.code
        page = 'pages/activity/detail/index?id={activity_id}&articleId={blog_id}'.format(activity_id=obj.activity.id, blog_id=obj.activity.blog_id)
        data = WeiXinData()
        data.set_key('thing1', obj.activity.title[:20]) # 20个字符
        date_format = '%m月%d日 %H:%M:00'
        data.set_key('date2', obj.activity.start_at.strftime(date_format))
        data = data.data
        for touser in openid_list:
            WeiXinSubscribeMessageApi().send(touser, template_id, page, data)
