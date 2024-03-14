import torch
import torch.optim as optim
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.metrics import mean_squared_error
from .models import h_net, a_net, standard_model
from .loss_functions import RU_loss, weighted_mse_loss
from .density_ratio_estimation import estimate_density_ratio

class StandardEstimator(BaseEstimator, RegressorMixin):
    def __init__(self, classifier, n_epochs=100, batch_size=10):
        self.classifier = classifier
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.model = standard_model()
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-2)
        self.losses = []

    def fit(self, X, y):
        X_train = torch.from_numpy(X).float().reshape(-1, 1)
        Y_train = torch.from_numpy(y).float().reshape(-1, 1)

        for epoch in range(self.n_epochs):
            for i in range(0, len(X_train), self.batch_size):
                Xbatch = X_train[i:i+self.batch_size]
                ybatch = Y_train[i:i+self.batch_size]

                density_ratios = torch.tensor([estimate_density_ratio(x.numpy(), self.classifier) for x in Xbatch], dtype=torch.float32)

                self.optimizer.zero_grad()
                predictions = self.model(Xbatch)
                loss = weighted_mse_loss(predictions, ybatch, density_ratios)
                loss.backward()
                self.optimizer.step()

                self.losses.append(loss.item())
        return self

    def predict(self, X):
        X_test = torch.from_numpy(X).float().reshape(-1, 1)
        with torch.no_grad():
            predictions = self.model(X_test)
        return predictions.numpy()

    def evaluate(self, X, y):
        predictions = self.predict(X)
        mse = mean_squared_error(y, predictions.squeeze())
        return mse

class RUEstimator(BaseEstimator, RegressorMixin):
    def __init__(self, gamma, classifier, n_epochs=100, batch_size=10):
        self.gamma = gamma
        self.classifier = classifier
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.h_model = h_net()
        self.a_model = a_net()
        self.optimizer = optim.Adam(list(self.h_model.parameters()) + list(self.a_model.parameters()), lr=1e-2)

    def fit(self, X, y):
        X_train = torch.from_numpy(X).float().reshape(-1, 1)
        Y_train = torch.from_numpy(y).float().reshape(-1, 1)
        self.LOSS = []

        for epoch in range(self.n_epochs):
            for i in range(0, len(X_train), self.batch_size):
                Xbatch = X_train[i:i+self.batch_size]
                ybatch = Y_train[i:i+self.batch_size]

                density_ratios = torch.tensor([estimate_density_ratio(x.numpy(), self.classifier) for x in Xbatch], dtype=torch.float32)

                self.optimizer.zero_grad()
                h_pred = self.h_model(Xbatch)
                a_pred = self.a_model(Xbatch)
                loss = RU_loss(h_pred, a_pred, self.gamma, ybatch, density_ratios)
                loss.backward()
                self.optimizer.step()

                self.LOSS.append(loss.item())
        return self

    def predict(self, X):
        X_test = torch.from_numpy(X).float().reshape(-1, 1)
        with torch.no_grad():
            predictions = self.h_model(X_test)
        return predictions.numpy()

    def evaluate(self, X, y):
        predictions = self.predict(X)
        mse = mean_squared_error(y, predictions.squeeze())
        return mse

