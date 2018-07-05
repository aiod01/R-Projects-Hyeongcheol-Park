import numpy as np
from sklearn.cluster import KMeans

class ImageQuantizer:

    def __init__(self, b):
        self.b = b # number of bits per pixel

    def quantize(self, img):
        """
        Quantizes an image into 2^b clusters

        Parameters
        ----------
        img : a (H,W,3) numpy array

        Returns
        -------
        quantized_img : a (H,W) numpy array containing cluster indices

        Stores
        ------
        colours : a (2^b, 3) numpy array, each row is a colour

        """

        H, W, _ = img.shape
        model = KMeans(n_clusters=2**self.b, n_init=3)#이 설정은 sikit에서 온 것이다.
        
        img2dim=img.reshape(H*W,3)
        model.fit(img2dim)
        colors=np.array(model.cluster_centers_).astype('uint8')#cluster_centers_는 sikit
        #에서 왔고, unit8은 type을 interger 로 바꾸는 것인데, astype은 type을 바꾸는 함수이다. 
        quantized_img=model.predict(img2dim).reshape((H,W))
        
        self.colors=colors

        return quantized_img

    def dequantize(self, quantized_img):
        H, W = quantized_img.shape
        img = np.zeros((H,W,3), dtype='uint8')

        for i in range(H):
            for j in range(W):
                img[i,j,:]=self.colors[quantized_img[i,j],:]#colors가 뭔지 모르겠어서 이 줄도 모르겠어

        return img
