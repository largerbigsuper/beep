from beep.bot.models import mm_BotComment, BotComment
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), 'bot/comment.txt')

comment_file_path = 'bot/comment.txt'

def load_data_from_file(fpath):
    comments = []
    with open(fpath) as f:
        for line in f.readlines():
            if line:
                comments.append(line.replace('\n', ''))
    return comments

def save_comments(comment_list):
    comments = []
    for text in comment_list:
        comment = BotComment(text=text)
        comments.append(comment)
    mm_BotComment.bulk_create(comments)


def run():
    comments = load_data_from_file(FILE_PATH)
    save_comments(comments)
    print('done')

