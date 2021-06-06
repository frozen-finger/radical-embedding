import torch as torch
import torch.nn as nn

class radical2vec(nn.Module):
    def __init__(self):
        super(radical2vec, self).__init__()
        #l1
        self.conv1 = nn.Conv2d(3, 64, 11, padding=2, stride=4)        #3 * 111 * 111
        self.norm1 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(3, 2)         #64*55*55
        #l2
        self.conv2 = nn.Conv2d(64, 192, 5, padding=2)        #192*55*55
        self.norm2 = nn.BatchNorm2d(192)
        self.pool2 = nn.MaxPool2d(3, 2)         #192*14*14

        #l3
        self.conv4 = nn.Conv2d(192, 256, 3, padding=1)      #256*27*27
        self.norm3 = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(256, 256, 3, padding=1)     #256*27*27
        self.norm4 = nn.BatchNorm2d(256)
        self.conv6 = nn.Conv2d(256, 192, 3, padding=1)      #192*27*27
        self.norm5 = nn.BatchNorm2d(192)
        self.pool3 = nn.MaxPool2d(3, 2)        #192*13*13
        self.conv7 = nn.Conv2d(192, 64, 1)     #64*13*13
        self.norm6 = nn.BatchNorm2d(64)
        self.pool4 = nn.MaxPool2d(3, 2)        #64*6*6

        #l4
        self.fc1 = nn.Linear(64*6*6, 4096)
        self.norm7 = nn.BatchNorm1d(4096)
        self.fc2 = nn.Linear(4096, 4096)
        self.norm8 = nn.BatchNorm1d(4096)
        self.fc3 = nn.Linear(4096, 100)
        self.fc4 = nn.Linear(100, 289)

        self.relu = nn.ReLU()

    def forward(self, X):
        output = self.conv1(X)
        output = self.norm1(output)
        output = self.relu(output)
        output = self.pool1(output)
        output = self.conv2(output)
        output = self.norm2(output)
        output = self.relu(output)
        output = self.pool2(output)
        output = self.conv4(output)
        output = self.norm3(output)
        output = self.relu(output)
        output = self.conv5(output)
        output = self.norm4(output)
        output = self.relu(output)
        output = self.conv6(output)
        output = self.norm5(output)
        output = self.relu(output)
        output = self.pool3(output)
        output = self.conv7(output)
        output = self.norm6(output)
        output = self.relu(output)
        output = self.pool4(output)
        output = output.view(-1, 64*6*6)
        output = self.fc1(output)
        output = self.norm7(output)
        output = self.relu(output)
        output = self.fc2(output)
        output = self.norm8(output)
        output = self.relu(output)
        output1 = self.fc3(output)
        output = self.relu(output1)
        output = self.fc4(output)
        return output, output1
if __name__ == '__main__':
    r2v = radical2vec()
    print(r2v)