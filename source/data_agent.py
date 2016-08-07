import os

import sys
sys.path.append('../facepy/feature_extraction/')



from image import extract_features

import numpy as np


data_dir = os.path.abspath('../data/')

mark_data = os.path.join(data_dir,"mark.data")

image_dir = os.path.join(data_dir,"pic/")

def get_data():
    return data_parse(mark_data)

def data_parse(mark_data):
    """

    :param mark_data: string
        path to the markdata
    :return: dict

        dict of dict, {id:{"imageName":imageName,"gender":gender,"fa_score":fa_score,"skin":skin,"glasses":glasses}}
        the outer dict's key is image Id, the item is a dict of description of
        this image
    """



    data = {}

    with open(mark_data,'r') as f:
        for line in f:
            id,imageName,gender,fa_score,skin,glasses = line.strip().split(" ")

            data[id] = {"imageName":imageName+".jpg","gender":gender,"fa_score":fa_score,"skin":skin,"glasses":glasses}

    return data

data = get_data()

def get_image_by_name(image_name):
    """

    :param imageID: string
        image name
    :return: string
        path of needed image
    """
    return image_retrive(image_name,image_dir)

def get_image_by_id(imageId):
    """
    :param data : dict
        {id:{"imageName":imageName,"gender":gender,"fa_score":fa_score,"skin":skin,"glasses":glasses}}

    :param imageId: string

    :return: string
        path of needed image
    """

    return image_retrive(data[imageId]["imageName"],image_dir)



def image_retrive(image_name,image_dir):
    """

    :param imageID: string
        image name
    :param image_dir: string
        dir path of image
    :return: string
        path of this image

    """
    return os.path.join(image_dir,image_name)



def get_image_Ids():
    return [Id for Id in data]

def get_image_names():
    return {Id:data[Id]["imageName"] for Id in data}

def get_image_names_only():
    return get_image_names().values()

def get_data_glasses():
    return {Id:data[Id]["glasses"] for Id in data}

def get_data_gender():
    return {Id:data[Id]["gender"] for Id in data}

def get_data_faScores():
    return {Id:data[Id]["fa_score"] for Id in data}

def get_data_skin():
    return {Id:data[Id]["skin"] for Id in data}


def persistent_image_features(images, toStoreFile):
    """
    extract features for images and store the numpy array into a file

    :images:list
        a list of strings which represents the  image file path

    :toStoreFile : string
        the file path to store the images features numpy array

    :return:
    """
    image_features = extract_features(images)

    np.save(toStoreFile, image_features)


def load_image_features(featuresFile):
    return np.load(featuresFile)


if __name__ =="__main__":
    image_names = get_image_names_only()

    image_paths = [get_image_by_name(image_name) for image_name in image_names]

    persistent_image_features(image_paths, "../data/image_features/image_features")
