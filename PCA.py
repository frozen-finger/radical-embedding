from sklearn.decomposition import PCA
import numpy as np
class PCA1:
    def __init__(self, components):
        self.pca = PCA(components)

    def transform(self, dataset):
        new = self.pca.fit_transform(dataset)
        return new