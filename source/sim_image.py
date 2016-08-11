# -*- coding:utf-8 -*-

import sys

sys.path.append('../facepy/feature_extraction/')

from image import extract_features
import fnmatch
import os
import numpy as np

from sklearn.neighbors import LSHForest

image_similar_dir = os.path.abspath('../data/image_similar/')

similar_image_paths = []
for file in os.listdir(image_similar_dir):
    if fnmatch.fnmatch(file, '*.jpg'):
        similar_image_paths.append(image_similar_dir +'/'+ file)


similar_image_paths.sort()

# extract features
#similar_image_features = extract_features(similar_image_paths)
#np.save('../data/model/similar_image.pickle',similar_image_features)

# load features

similar_image_features = np.load('../data/model/similar_image.pickle.npy')

lshf = LSHForest(random_state=42)
lshf.fit(similar_image_features)
def find_similar_image(image_path):
    image_feature = extract_features([image_path])
    distances, indices = lshf.kneighbors(image_feature, n_neighbors=3)
    return [similar_image_paths[i] for i in indices[0]][1:]


if __name__ == '__main__':

    image_path = image_similar_dir + '/2015110420陈美玉.jpg'
    similar_images = find_similar_image(image_path)

    print similar_images
