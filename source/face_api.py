# -*- coding: utf-8 -*-
#
import os, os.path
import uuid
import hashlib
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options


from face_profile import get_profile

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            debug=True,
            img_dir='./imgs'    #这儿改成想要存图片的地址
        )
        super(Application, self).__init__(handlers, **settings)
        self.maybe_create_dir()

    def maybe_create_dir(self):
        img_dir = self.settings.img_dir
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)


class BaseHandler(tornado.web.RequestHandler):

    def get_img_path(self, filename):
        return os.path.join(self.settings["img_dir"], filename)

    def gen_unique_name(self):
        return hashlib.md5(str(uuid.uuid4())).hexdigest()

    def image_profile(self, image_path):
        #实现函数image_profile

        return get_profile(image_path)

    def find_simlilar_image(self, file_path, samegender=False):
        #实现函数find_simlilar_image
        return file_path+'.new'


class MainHandler(BaseHandler):

    #curl -F img=@ThisImgName.jpg http://localhost:8888/?action=uploadImg
    #curl -d '{"samegender":"0","imgpath":"fdsfasfsd"}' http://localhost:8888/?action=getSimilar

    def get(self):
        self.set_status(404)

    def post(self):
        action = self.get_query_argument('action')
        if action == 'uploadImg':
            self.receive_img()
        elif action == 'getSimilar':
            self.get_similar_img()
        else:
            self.set_status(404)

    def receive_img(self):
        print self.request.files
        http_file_list = self.request.files.get('img')
        if http_file_list:
            f = http_file_list[0]
            filename = self.gen_unique_name()
            filepath = self.get_img_path(filename)
            try:
                with open(filepath, 'wb') as up:
                    up.write(f.body)
            except Exception, e:
                self.set_status(500)
                return self.write('save img error')
            retd = self.image_profile(filepath)
            self.write(tornado.escape.json_encode(retd))
        else:
            self.set_status(404)
            self.write('no file found')


    def get_similar_img(self):
        try:
            dinfo = tornado.escape.json_decode(self.request.body)
            if not dinfo:
                raise ValueError
            imgpath = dinfo.get('imgpath')
            samegender = dinfo.get('samegender')
            if not (imgpath and samegender):
                raise ValueError
            samegender = False if samegender in [0, '0'] or samegender.lower() == 'false' else True
        except:
            self.set_status(404)
            return self.write('argument error')
        newpath = self.find_simlilar_image(imgpath, samegender)
        self.write({'newimg': newpath})



def main():
    tornado.options.parse_command_line()
    print 'will listening on port %s...' % options.port
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()