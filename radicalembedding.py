import torch.nn.functional as F
import numpy as np
import torch as torch
import torch.optim as optim
from torch.utils.data import DataLoader
from dataload import rdataset
from model import radical2vec

iopair = []
with open("chindexpair.txt", encoding='utf-8') as f:
    lines = f.readlines()
for line in lines:
    line = line.strip('\n').split('\000')
    iopair.append(line)

mydataset = rdataset("totalpair.txt")
testdataset = rdataset("testindexpair.txt")
traindata = DataLoader(mydataset, batch_size=4, shuffle=True)
testdata = DataLoader(testdataset, batch_size=4, shuffle=True)
model = radical2vec().cuda()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

for epoch in range(50):
    sum_loss = 0.0
    for data in traindata:
        x, y = data
        x = x.cuda()
        y = y.cuda()
        pred, embed = model(x)
        optimizer.zero_grad()
        loss = F.cross_entropy(pred, y)
        loss.backward()
        optimizer.step()
        sum_loss+=loss
    with open("log1", 'a') as f:
        f.write("{0},{1}".format(epoch, sum_loss)+"\n")
    print("epoch{0}, loss {1}".format(epoch, sum_loss))

torch.save(model.state_dict(), 'model_total.pth')

# correct = 0
# total = 0
# with torch.no_grad():
#     model.load_state_dict(torch.load('model.pth'))
#     for data in testdata:
#         x, y = data
#         x = x.cuda()
#         y = y.cuda()
#         pred, embed = model(x)
#         pred = torch.argmax(pred, 1)
#         correct += (pred==y).sum().item()
#         total += pred.size(0)
# print("correct/total:{}".format(correct/total))
