import praw
import string
import markovutils

UserAgent = "mac:VoiceofReddit:v0.1 (by /u/tbasherizer)"


def main():
    reddit = praw.Reddit(user_agent=UserAgent)
    posts = reddit.get_subreddit('all').get_hot(limit=10)
    comments = []
    for post in posts:
        post.replace_more_comments()
        comment_list = praw.helpers.flatten_tree(post.comments)
        post_comments = []
        post_sum = 0
        for comment in comment_list:
            post_comments.append(comment)
            post_sum += comment.score
        post_average = post_sum / len(comment_list)
        for comment in post_comments:
            if (comment.score > post_average):
                comments.append(comment.body)

    markovmodel = markovutils.MarkovModel([comment.split() for comment in comments],depth=1)
    print string.join(markovmodel.generate())
markovmodel = main()
