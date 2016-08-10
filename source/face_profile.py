# -*- coding:utf-8 -*-
import pickle

import sys
sys.path.append('../facepy/feature_extraction/')
from image import extract_features

glasses_svm = pickle.load(open("../data/model/glasses_SVM.pickle",'rb'))

fa_score_svm = pickle.load(open("../data/model/fa_score_SVM.pickle",'rb'))
skin_svm = pickle.load(open("../data/model/skin_SVM.pickle",'rb'))

def get_profile(image):

    result = {}

    features = extract_features([image])

    glasses_result = glasses_svm.predict(features)[0]
    fa_score_result = fa_score_svm.predict(features)[0]
    skin_score = skin_svm.predict(features)[0]

    if glasses_result == 0:
        result["glasses"] = "无"
    else:
        result["glasses"] = "有"

    result['face_score'] = fa_score_result

    if skin_score ==-1:
        result["skin"] = "偏黑"
    elif skin_score == 0:
        result["skin"] = "正常"
    else:
        result["skin"] = "偏白"

    return result


    
