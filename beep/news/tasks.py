from config.celery import app

from utils.post.gen_post import Post
from .models import News, mm_News, mm_CrawledDocument


@app.task
def update_news_from_crawler():
    """将爬虫结果更新到快讯模块
    """

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
    news_list = mm_News.bulk_create(objs)

    for news in news_list:
        news.post = Post().generate_post(news.title, news.published_at, news.content)
        news.save()


