import os
from gensim.models import word2vec
from character_crawl import crawl
from PCA import PCA1
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from model import radical2vec
import torch as torch
from PIL import Image
import torchvision.transforms as transforms
from visdom import Visdom

mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']
def ischaracter(text):
    if len(text) == 1:
        return all('\u4e00' <= char <= '\u9fff' for char in text)
    else:
        return False

with open("in_the_name_of_people.txt", encoding="utf-8") as f:
    lines = f.readlines()

dataset = []
for line in lines:
    line = line.strip()
    a = []
    for ch in line:
        if ischaracter(ch):
            a.append(ch)
    dataset.append(a)
dic = {}
count = 0
for i in range(len(dataset)):
    for j in range(len(dataset[i])):
            dic[dataset[i][j]] = 1
#
chbushoupair = {}
with open("chbushoupair.txt",  encoding='utf-8') as f:
    lines = f.readlines()
for line in lines:
    pair = line.strip("\n").split("\000")
    chbushoupair[pair[0]] = pair[1]
#
# for i in dic:
#     if count>=2606:
#         res = crawl(i)
#         if res and res['bushou'] in chbushoupair:
#             with open("testindexpair.txt", 'a', encoding='utf-8') as f:
#                 f.write(i+'\000{}'.format(chbushoupair[res['bushou'].strip('\n')])+'\n')
#     count+=1

# with open("C:/Users/99388/Desktop/Unicodecharacter.txt", encoding='utf-8') as f:
#     lines = f.readlines()
# totalch = {}
# for line in lines:
#     for ch in line:
#         res = crawl(ch)
#         if res and res['bushou'] in chbushoupair:
#             totalch[ch] = chbushoupair[res['bushou'].strip('\n')]
# with open("totalpair.txt", 'a', encoding='utf-8') as f:
#     for i in totalch:
#         f.write(i+"\000"+totalch[i]+"\n")



# for i in dic:
#     res = crawl(i)
#     if res:
#         with open("chindexpair.txt", 'a', encoding='utf-8') as f:
#             f.write(i+'\000{}'.format(chbushoupair[res['bushou']])+'\n')

# count = 0
# with open("bushoulist.txt", encoding='utf-8') as f:
#     lines = f.readlines()
# line = lines[0].strip().split("\000")
# with open("chbushoupair.txt", 'a', encoding='utf-8') as f:
#     for i in range(len(line)):
#         f.write(line[i]+"\000{}".format(i)+"\n")

# model = word2vec.Word2Vec(sentences=dataset, min_count=1)
# model.save("wordin.model")
model = word2vec.Word2Vec.load("wordin.model")
rmodel = radical2vec()
rmodel.load_state_dict(torch.load("model_total.pth"))
rmodel.eval()
picturepath = "C:/Users/99388/Desktop/Character/"
embdediings = []
rembeddings = []
lines = []
# for i in dic:
#     res = crawl(i)
#     if res and res['bushou'] == "扌":
#         with open("analyzesimilarity.txt", "a", encoding='utf-8') as f:
#             f.write(i)

# with open("in_the_name_of_people.txt",  encoding='utf-8') as f:
#     lines = f.readlines()
for ch in dic:
    # for ch in line:
        if os.path.isfile(picturepath+ch+".png"):
            lines.append(ch)
            with torch.no_grad():
                im = Image.open(picturepath+ch+".png")
                im = im.convert("RGB")
                im = transforms.ToTensor()(im)
                im = im.unsqueeze(0)
                _, rembed = rmodel(im)
                rembed = rembed[0]
                rembeddings.append(np.array(rembed))
            embdediings.append(model.wv.get_vector(ch))
embdediings = np.array(embdediings)
for i in range(len(embdediings)):
    emax = np.max(embdediings[i])
    emin = np.min(embdediings[i])
    rmax = np.max(rembeddings[i])
    rmin = np.min(rembeddings[i])
    rembeddings[i] = (rembeddings[i]-rmin)/(rmax-rmin)
    embdediings[i] = (embdediings[i]-emin)/(emax-emin)
# embdediings = np.concatenate((embdediings, rembeddings), axis=1)
pca = PCA1(2)
newembeddings = pca.transform(rembeddings)
plt.scatter(x=newembeddings[:, 0], y=newembeddings[:, 1])
# newembeddings = newembeddings*100
# fig = plt.figure()
# ax1 = fig.gca(projection="3d")
# for t in range(len(newembeddings)):
#     ax1.scatter3D(newembeddings[t][0], newembeddings[t][1], newembeddings[t][2])
#     # ax1.text(newembeddings[t][0], newembeddings[t][1], newembeddings[t][2]+0.01, lines[0][t])
#     ax1.text(newembeddings[t][0], newembeddings[t][1], newembeddings[t][2] + 0.01, lines[t])
plt.show()

# with open("C:/Users/99388/PycharmProjects/radicalembedding/log") as f:
#     lines = f.readlines()
# with open("C:/Users/99388/PycharmProjects/radicalembedding/log1") as f:
#     lines1 = f.readlines()

# f1, f2 = [], []
# for i in range(50):
#     l = lines[i].strip('\n').split(',')
#     l1 = lines1[i].strip('\n').split(',')
#     l[0] = int(l[0])
#     l[1] = float(l[1])
#     l1[0] = int(l1[0])
#     l1[1] = float(l1[1])
#     f1.append(l)
#     f2.append(l1)
# f1 = np.array(f1)
# f2 = np.array(f2)
# env = Visdom()
# assert env.check_connection()
# env.line(
#     X=f2[:, 0],
#     Y=f2[:, 1],
# )
# plt.plot(f1[:, 0], f1[:, 1])
# plt.grid(b=True, which='both')
# plt.show()

# print(model.wv.similarity('', '提'))
# dicbushou = {}
# for i in dic:
#     res = crawl(i)
#     if res and res['bushou'] not in dicbushou:
#         dicbushou[res['bushou']] = 1
#
# with open("bushoulist.txt", 'a', encoding='utf-8') as f:
#     for j in dicbushou:
#         f.write(j+"\000")
# with open("bushoulist.txt", encoding='utf-8') as f:
#     lines = f.readlines()
#     lines = lines[0].strip().split("\000")
#     print(len(lines))

