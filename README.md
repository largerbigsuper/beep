# beep project

## 初始化项目

```
# 创建超级管理员
docker-compose -f dev.yml run --rm  django python manage.py createsuperuser

# 初始化地区
docker-compose -f dev.yml run --rm  django python manage.py runscript init_area

```

## 常用命令


**工程相关**

```shell
django-admin startapp --template ../templates/app_template appname


```

**管理命令**

```
docker-compose -f dev.yml run --rm  django python manage.py createsuperuser
```

## TODO LIST

- [x] 评论分级列表
- [ ] es搜索功能
- [ ] 微信信息回调
- [ ] 聊天服务器搭建
- [x] 活动查看详情增加浏览次数
- [x] 活动报名增加到行程表中
- [x] 活动收藏
- [x] 评论点赞
- [x] 博文热门接口
- [x] 博文关注列表
- [x] 博文增加用户关系是否关注
- [x] 用户增加简介字段
- [x] 活动详情中显示是否已经报名
- [x] 用户支持查询
- [x] 粉丝列表增加是否关注
- [x] 评论列表增加博文详情
- [x] 二级评论列表
- [x] 用户博文个数，粉丝数量，关注数量 

## 2019-10-18

- [x] 发短信接口[登陆| 注册| 找回密码]
- [x] 短信登陆
- [x] 短信注册



- [x] 快讯分享图片动态生成

- [x] 博文转发功能
- [x] 博文话题 拓展新人榜，专题榜

- [x] 我的粉丝/关注列表搜索报错


## 2019-10-20

- [ ] 博文搜索
- [ ] 微信服务号 直播推送
- [ ] 群直播接入
- [ ] 小程序授权登陆
- [ ] 红V蓝V身份设置
- [ ] 图片加水印
- [x] 站点支持https
- [ ] 活动增加审核状态

