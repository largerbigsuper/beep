# beep project

## 配置文件

- `dev.yml` 测试环境部署
- `production.yml` 正式环境部署

## 重要文件

```
# .env 需添加至项目根目录，没有版本跟踪
# 数据库信息
DB_HOST=localhost
DB_PORT=3306
DB_NAME=beep_db_local
DB_USER=root
DB_PASSWORD=Password123/
```

## 初始化项目

```
# 创建超级管理员
docker-compose -f dev.yml run --rm  django python manage.py createsuperuser

# 初始化地区
docker-compose -f dev.yml run --rm  django python manage.py runscript init_area
```

## 常用命令


**管理命令**

```
docker-compose -f dev.yml run --rm  django python manage.py createsuperuser
```

**启动命令**

```
docker-compose -f dev.yml build

docker-compose -f dev.yml up -d

docker-compose -f dev.yml stop
```

**服务缩放**

```
docker-compose -f dev.yml scale celery_worker=4
```

## TODO LIST

- [x] 评论分级列表
- [x] 微信信息回调
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

- [x] 微信服务号 直播推送
- [x] 群直播接入
- [x] 小程序授权登陆
- [x] 红V蓝V身份设置
- [x] 图片加水印
- [x] 站点支持https
- [x] 活动增加审核状态


## 2019-10-23 为题汇总

- [x] 我的博文/我的关注 博文排序按照时间倒叙排 
- [x] 我的博文增加置顶功能


### 前端问题


### 需求不明确

- 给一个积分系统， 积分产生/消费。


## 2019-10-24 任务

- [x] 七牛云域名临时更换为 `imgbeepcrypto.lhxq.top`
- [x] 活动区域选择 变更为 xxx省， 海外[全国]
- [x] 我的博文，我的关注博文排序
- [x] 我的博文增加置顶功能， 限制1个
- [x] 发布活动关联一个博文
- [x] 我的关注不显示匿名博文

## 2019-10-25 任务

- [x] wehub回调服务
- [x] 群直播功能

## 2019-10-26 任务

- [x] 我的微博列表中没有转发微博信息

## 2019-10-29

- [x] 活动创建时封面图不能传文件类型，需传字符串类型
- [x] 后台创建的活动没有绑定博文
- [x] 活动地区查询根据城市名称 其他, 海外
- [x] 转发博文列表中没有显示转发的博文

## 2019-10-30
- [x] 直播群与活动绑定
- [x] 群直播增加历史消息
- [x] 群成员更新到用户表
- [x] 用户消息记录
- [x] 历史记录增加用户信息
- [x] 用户提问推送到微信

## 2019-10-31

- [x] 收到的评论| @我的 |收到的赞 返回原始博文信息


## 2019-11-01

- [x] 搜索记录不加分词
- [x] 专题增加sub_title
- [x] 增加抽奖功能
- [x] 通过用户名查用户信息

## 2019-11-05

- [x] 评论用户存储数据错误