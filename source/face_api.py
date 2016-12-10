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

from sim_image import find_similar_image

define("port", default=8888, help="run on the given port", type=int)

image_dir = os.path.abspath('../data/receive_image')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/images/(.*)", tornado.web.StaticFileHandler, {'path':r"../data/receive_image/"}),
            (r"/", MainHandler),
        ]
        settings = dict(
            debug=True,
            img_dir=image_dir    #这儿改成想要存图片的地址
        )
        super(Application, self).__init__(handlers, **settings)
        self.maybe_create_dir()

    def maybe_create_dir(self):
        img_dir = self.settings['img_dir']
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)


class BaseHandler(tornado.web.RequestHandler):

    def get_img_path(self, filename):
        return os.path.join(self.settings["img_dir"], filename)

    def gen_unique_name(self):
        return hashlib.md5(str(uuid.uuid4())).hexdigest()

    def image_profile(self, image_path):

        return get_profile(image_path)

    def find_simlilar_image(self, file_path):
        #实现函数find_simlilar_image
        return find_similar_image(file_path)


class MainHandler(BaseHandler):

    #curl -F img=@ThisImgName.jpg http://localhost:8888/?action=uploadImg
    #curl -d '{"samegender":"0","imgpath":"fdsfasfsd"}' http://localhost:8888/?action=getSimilar

    def get(self):
        img = self.get_query_argument('img')
        self.send_image(img)

    def post(self):
        action = self.get_query_argument('action')
        if action == 'uploadImg':
            self.receive_img()
        elif action == 'getSimilar':
            self.get_similar_img()
        #elif action.endwith(".jpg"):
            #self.send_image(action)
        else:
            self.set_status(404)

    def send_image(self,imageName):
        imagePath = self.get_img_path(imageName)
        self.write({"imageName":imagePath})
    def receive_img(self):
        print self.request.files
        http_file_list = self.request.files.get('img')
        if http_file_list:
            f = http_file_list[0]
            filename = self.gen_unique_name()
            filepath = self.get_img_path(filename)+".jpg"
            try:
                with open(filepath, 'wb') as up:
                    up.write(f.body)
            except Exception, e:
                self.set_status(500)
                return self.write('save img error')
            retd = self.image_profile(filepath)
            print 'save image to '+ filepath
            retd['imagePath'] = filepath
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
            if not imgpath:
                raise ValueError
        except:
            self.set_status(404)
            return self.write('argument error')
        newpath = self.find_simlilar_image(imgpath)
        self.write({'newimg': newpath})



def main():
    tornado.options.parse_command_line()
    print 'will listening on port %s...' % options.port
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
