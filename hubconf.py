
"""# Import libraries"""

import torch
import torchvision
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor
import numpy as np

"""# Define new labels"""

new_labels = {
    0: 'Upper',
    1: 'Lower',
    2: 'Feet',
    3: 'Bag'
}

"""# Define label mapping"""

label_mapping = {
    0: [0, 1, 4, 6],
    1: [2, 3],
    2: [5, 7, 9],
    3: [8]
}

"""# Load the Fashion-MNIST dataset and apply new labels"""

fmnist_train = FashionMNIST(root="./data", train=True, download=True, transform=ToTensor())
fmnist_test = FashionMNIST(root="./data", train=False, download=True, transform=ToTensor())

new_train_data = []
new_train_labels = []
new_test_data = []
new_test_labels = []

"""# Map the original labels to new labels"""

for i, (data, label) in enumerate(fmnist_train):
    for new_label, orig_labels in label_mapping.items():
        if label in orig_labels:
            new_train_data.append(data)
            new_train_labels.append(new_label)
            break

for i, (data, label) in enumerate(fmnist_test):
    for new_label, orig_labels in label_mapping.items():
        if label in orig_labels:
            new_test_data.append(data)
            new_test_labels.append(new_label)
            break

"""# Convert the data and labels to PyTorch tensors"""

new_train_data = torch.stack(new_train_data, dim=0)
new_train_labels = torch.tensor(new_train_labels)
new_test_data = torch.stack(new_test_data, dim=0)
new_test_labels = torch.tensor(new_test_labels)

"""# Create the custom dataset"""

class CustomFashionMNIST(torch.utils.data.Dataset):
    def __init__(self, data, labels):
        super(CustomFashionMNIST, self).__init__()
        self.data = data
        self.labels = labels
    
    def __getitem__(self, index):
        return self.data[index], self.labels[index]
    
    def __len__(self):
        return len(self.data)

train_dataset = CustomFashionMNIST(new_train_data, new_train_labels)
test_dataset = CustomFashionMNIST(new_test_data, new_test_labels)

"""# Reconfigure the neural network"""

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.fc1 = torch.nn.Linear(320, 50)
        self.fc2 = torch.nn.Linear(50, 4) # 4 neurons for the 4 new labels
    
    def forward(self, x):
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv1(x), 2))
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 320)
        x = torch.nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.nn.functional.log_softmax(x, dim=1)

net = Net()

criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(net.parameters(), lr=0.01, momentum=0.5)

"""# Train the neural network"""

train_loader = torch.utils.data
