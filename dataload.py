import torch as torch
import torchvision.transforms as transforms
from torch.utils.data import Dataset
import numpy as np
from torch.utils.data import DataLoader
from PIL import Image

class rdataset(Dataset):
    def __init__(self, pairpath):
        self.imagepath = "C:/Users/99388/Desktop/Character"
        self.pairpath = pairpath
        self.dic = {}
        self.set1 = []
        self.n_samples = 0
        with open(self.pairpath, encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            self.n_samples+=1
            line = line.strip('\n').split('\000')
            self.set1.append(line[0])
            self.dic[line[0]] = int(line[1])

    def __getitem__(self, item):
        path = self.imagepath+'/'+self.set1[item]+".png"
        im = Image.open(path)
        im = im.convert("RGB")
        im = transforms.ToTensor()(im)
        target = self.dic[self.set1[item]]
        target = torch.tensor(target, dtype=torch.long)
        return im, target

    def __len__(self):
        return self.n_samples

if __name__ == '__main__':
    data = rdataset()
    for i in range(data.__len__()):
        print(data.__getitem__(i)[0].shape, data.__getitem__(i)[1].shape)