"""Define structures to manage and interface a fully connected neural network for UTKfaces."""

import numpy as np
from sklearn.model_selection import StratifiedKFold

#Pytorch 
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset

#Ray tune
from ray import train, tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.hyperopt import HyperOptSearch

from functools import partial

class UtkDataset(Dataset):
    """Pytorch dataset to handle adult data."""
    def __init__(self, data):
        """Make data conversion for pytorch integration.

        :param data: dataset to convert.
        :type data: dictionary of numpy.ndarray
        """
        self.y = torch.from_numpy(data["y"]).type(torch.float)
        self.x = torch.from_numpy(data["x"]).type(torch.float)

    def __len__(self):
        """Length of dataset."""
        return len(self.y)

    def __getitem__(self, idx):
        """Fetch ith data point.

        :param idx: Data index.
        :type idx: int or array of int
        """
        return self.x[idx], self.y[idx]

class CNN(nn.Module):
    """Pytorch convulutional neural network for UTKfaces."""
    def __init__(self, input_size, c,l1, l2, output_size):
        """Sets layers for a neural network.

        :param input_size: Number of features.
        :type input_size: int
        :param c: Number channels after convolution.
        :type c: int
        :param l1: Size of the first layer.
        :type l1: int
        :param l2: Size of the second layer.
        :type l2: int
        :param output_size: Number classes in the labels.
        :type output_size: int
        """

        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, c, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(c*6*6, l1)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(l1, l2)
        self.fc3 = nn.Linear(l2, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """Forward pass in the neural network.

        :param x: Data points.
        :type x: torch.tensor
        :return: Neural network function applied to x.
        :rtype: torch.tensor
        """
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

class UtkNN:
    """Wrapper arround pytorch neural network. Interfare for hyper parameter optimisation using raytune."""
    def __init__(self):
        self.trained = False

    def fit(self, data):
        """Train and tune hyper parameters.
        
        :parameter data: Dataset the will be split for training and hyper parameter tuning. Dataset must contain a column called "PINCP" used as training label.
        :type data: Dictionary of numpy.ndarray
        """

        search_space = {
                "c": tune.choice([2 ** i for i in range(9)]),
                "l1": tune.choice([2 ** i for i in range(9)]),
                "l2": tune.choice([2 ** i for i in range(9)]),
                "lr": tune.loguniform(1e-4, 1e-1),
                "batch_size": tune.choice([8, 16, 32, 64, 128])
                }

        asha_scheduler = ASHAScheduler(
                time_attr='training_iteration',
                metric='loss',
                mode='min',
                max_t=100,
                grace_period=10,
                reduction_factor=3,
                brackets=1
                )

        hyperopt_search = HyperOptSearch(search_space, metric="loss", mode="min")

        tune_config = tune.TuneConfig(
                num_samples=20,
                scheduler=asha_scheduler,
                search_alg=hyperopt_search
                )

        tuner = tune.Tuner(
                partial(_train,data=data,stand_alone=False),
                tune_config=tune_config
                )

        results = tuner.fit()

        #Real training on full train dataset (no validation)
        #Using best hyper parameters 
        best_trial = results.get_best_result(metric="loss",mode="min")
        self.model = _train(best_trial.config, data=data, stand_alone=True)
        self.trained=True

    def predict(self, data):
        """Use a trained CNN to predict label of dataset.

        :param data: Dataset without label.
        :type data: numpy.ndarray
        :return: Prediction.
        :rtype: numpy.ndarray
        """
        if not(self.trained):
            raise AssertionError(f"{self} must be trained prioir to predict")
        with torch.no_grad():
           x = torch.from_numpy(x).float()
           y = np.argmax(self.model(x).cpu().numpy(),axis=1)
        return y

def _images_to_dataset(data):
    """Split images dataset into training and validation and convert into pytorch dataset.

    :param data: Dataset that will be split for validation.
    :type data: pandas.dataframe
    :return: Training and validation dataset (train,validation).
    :rtype: tuple of torch.utils.data.dataset
    """
    skf = StratifiedKFold(shuffle=True,random_state=123)
    for train,validation in skf.split(data,data["PINCP"]):
        pass
    train_dataset = UtkDataset(data.iloc[train])
    validation_dataset = UtkDataset(data.iloc[validation])
    return train_dataset, validation_dataset

def _train(config, data, stand_alone=False):
    """Train TabularNN with ray_tune hyper parameter tuning.

    :param data: Dataset that will be split for validation.
    :type data: pandas.dataframe
    :param stand_alone: (Optional default=False) If True _train does not use ray.tune and return the trained model. All the data provided is used in training without validation split.
    :type return_model: bool
    """
    net = CNN(len(data.columns)-1,config["l1"],config["l2"],2)

    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda:0"
    net.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=config["lr"])

    if stand_alone:
        train_dataset = AdultDataset(data)
    else:
        train_dataset, validation_dataset = _pandas_to_dataset(data)

    torch.manual_seed(1234)
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=8
    )
    if not(stand_alone):
        torch.manual_seed(1234)
        validation_loader = torch.utils.data.DataLoader(
        validation_dataset, batch_size=int(config["batch_size"]), shuffle=True, num_workers=8
    )

    for epoch in range(0, 10):  # loop over the dataset multiple times
        running_loss = 0.0
        epoch_steps = 0
        for i, batch_data in enumerate(train_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = batch_data
            inputs, labels = inputs.to(device), labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels.long())
            loss.backward()
            optimizer.step()

        if not(stand_alone):
            # Validation loss
            val_loss = 0.0
            val_steps = 0
            total = 0
            correct = 0
            for i, data in enumerate(validation_loader, 0):
                with torch.no_grad():
                    inputs, labels = data
                    inputs, labels = inputs.to(device), labels.to(device)

                    outputs = net(inputs)
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

                    loss = criterion(outputs, labels.long())
                    val_loss += loss.cpu().numpy()
                    val_steps += 1

            #Report back to Raytune
            train.report({"loss":val_loss/val_steps})

    if stand_alone:
        return net
