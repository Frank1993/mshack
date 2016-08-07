# 利用tensorflow来提取特征

## Inception

google在ImageNet比赛中训练了一个名为Inception的深度学习模型,这一模型可以在tensorflow中使用.
因此我们可以抽取该模型的前数层用来提取图片特征,仅仅重新训练最后一层即可.这可以极大地节约我们开发类似产品的时间.

tensorflow提供了一个相关[教程](https://www.tensorflow.org/versions/r0.9/how_tos/image_retraining/index.html)
其相关代码地址在[github](tensorflow/tensorflow/examples/image_retraining/retrain.py)上

一篇相关[论文](http://arxiv.org/pdf/1310.1531v1.pdf)

一篇极佳的相关[博客](http://www.kernix.com/blog/image-classification-with-a-pre-trained-deep-neural-network_p11)


关于inception-v3z中的'DecodeJpeg/contents:0'可见stackoverflow上的这个[回答](http://stackoverflow.com/questions/34484148/feeding-image-data-in-tensorflow-for-transfer-learning)