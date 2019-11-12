from config.celery import app

from utils.post.gen_poster import Post
from .models import News, mm_News, mm_CrawledDocument


@app.task
def update_news_from_crawler():
    """将爬虫结果更新到快讯模块
    """
    last_news = mm_News.all().order_by('-id').first()
    updates = mm_CrawledDocument.filter(is_news=False).order_by('published_at')[:10]
    updates_id = []
    objs = []
    for doc in updates:
        updates_id.append(doc.id)
        obj = News(title=doc.title,
                   content=doc.content,
                   origin='' if doc.source == '币世界' else  doc.source,
                   published_at=doc.published_at,
                   status=mm_News.STATUS_PUBLISHED)
        objs.append(obj)
    mm_CrawledDocument.filter(pk__in=updates_id).update(is_news=True)
    mm_News.bulk_create(objs)

    if not last_news:
        added_news = mm_News.all()
    else:
        added_news = mm_News.filter(pk__gt=last_news.id)
    for news in added_news:
        print('news_id: {}'.format(news.id))
        generate_poster.delay(news.id)


@app.task
def generate_poster(news_id):
    news = mm_News.filter(pk=news_id).first()
    if news:
        post = Post().generate_post(news.title, news.published_at, news.content, 2)
        # 不能通过save()保存
        mm_News.filter(pk=news.id).update(post=post)


