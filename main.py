import configparser
import random

import praw

from completed_comments import Comments


def login(config: configparser.ConfigParser) -> praw.Reddit:
    return praw.Reddit(username=config['DEFAULT']['username'],
                       password=config['DEFAULT']['password'],
                       client_id=config['DEFAULT']['client_id'],
                       client_secret=config['DEFAULT']['client_secret'],
                       user_agent="Berates /u/Orpherischt for his nonsense v0.1")


def mainloop(bot: praw.Reddit, bad_guys_name: str, bot_name: str, subreddit_name: str):
    db = Comments()
    subreddit = bot.subreddit(subreddit_name)
    for comment in subreddit.stream.comments():
        if db.exists(comment.id):
            continue
        elif comment.author == bot_name:
            continue
        # Dealing with his nonsense
        elif comment.author == bad_guys_name and comment.is_root:
            print('  He Posted some nonsense, dealing with him >:(')
            comment.reply("Bad Bot")
            db.add(comment.id)
        # Dealing with friend
        elif comment.body.lower() == "good bot" and comment.parent().author == bot_name:
            print('  Replying to friend')
            response = random.choice(['Anytime human :D', 'Shot bru!', '<3'])
            comment.reply(response)
            db.add(comment.id)
        # Dealing with hecklers
        elif comment.body.lower() == "bad bot" and comment.parent().author == bot_name:
            print('  Replying to heckler')
            comment.reply('[Thank you for your useful input on this matter]'
                          '(https://www.youtube.com/watch?v=P2AJKc82PDk)')
            db.add(comment.id)
    db.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('secrets.cfg')
    bot = login(config)
    mainloop(bot, config['DEFAULT']['spammers_name'], config['DEFAULT']['my_name'], config['DEFAULT']['subreddit_name'])
