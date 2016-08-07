# -*- coding:utf-8 -*-
import os
from six.moves import urllib
import tarfile
import sys
import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np


def create_graph(model_path = None):
    if model_path ==None:
        #如果不指定训练模型,则自动下载inception-v3到该文件所在目录
        model_dir = os.path.join(os.getcwd(),'inception_model')
        model_path = os.path.join(model_dir,'classify_image_graph_def.pb')
        if not os.path.exists(model_path):
            maybe_download_and_extract(model_dir)

    with gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')




def maybe_download_and_extract(model_dir):
    """Download and extract model tar file."""

    DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
    dest_directory = model_dir
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(dest_directory, filename)
    print model_dir
    print filepath
    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                filename, float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()
        filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
        print()
        statinfo = os.stat(filepath)
        print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)



create_graph()


def extract_features(images):
    """
    将图片转换成为numpy表示的特征数组,每行表示一张图片的feature
    images是一个列表,每个元素表示一张图片的绝对地址
    :param images: list of images' file path
    :return image_features: numpy represent of extracted features
    """

    #提取特征的维度
    nb_features = 2048
    image_features = np.empty((len(images),nb_features))



    with tf.Session() as sess:
        next_to_last_tensor = sess.graph.get_tensor_by_name('pool_3:0')
        for ind, image in enumerate(images):
            if len(images)>100 and(ind%100 == 0):
                print 'Processing %s...' % (image)

            if not gfile.Exists(image):
                tf.logging.fatal('File does not exist %s', image)
                continue

            image_data = gfile.FastGFile(image, 'rb').read()
            predictions = sess.run(next_to_last_tensor,{'DecodeJpeg/contents:0': image_data})
            image_features[ind,:] = np.squeeze(predictions)

    return image_features
