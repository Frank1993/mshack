# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from datetime import datetime
import json
import os
import pickle

from face_profile import get_profile
import codecs


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


    def post(self):
        data=json.loads(self.request.body)
        #newsId can be string or long
        newsId=data['NewsId']
        url=data['Url']
        title=None
        if 'Title' in data:
            title=data['Title']
        content=None
        if 'Content' in data:
            content=data['Content']
        similarNews=newsHasher.find_similar_news(content=content,newsId=newsId)
        response={'SimilarNews':similarNews}
        self.logging(newsId,url,title,content,similarNews)
        self.write(json.dumps(response))




application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    newsHasher=NewsHasher(tolerance=15)
    application.listen(8767)
    print 'listen'
    tornado.ioloop.IOLoop.current().start()





