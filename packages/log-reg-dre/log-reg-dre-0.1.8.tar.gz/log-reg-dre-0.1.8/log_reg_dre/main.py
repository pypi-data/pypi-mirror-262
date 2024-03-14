import numpy as np
from .data_generation import generate_x_vals
from .density_ratio_estimation import train_logistic_ratio_classifier, estimate_density_ratio
from .models import h_net, a_net, standard_model
from .loss_functions import RU_loss, weighted_mse_loss
from sklearn.metrics import mean_squared_error
import torch
import matplotlib.pyplot as plt
from .estimators import StandardEstimator, RUEstimator

P_TRAIN = 0.1
P_TEST = 0.9
NUM_PTS = 70
gamma_values = [2, 6, 18]

x_train = generate_x_vals(P_TRAIN, NUM_PTS)
x_test = generate_x_vals(P_TEST, NUM_PTS)
Y_train = np.log10(x_train) + np.sin(x_train) + np.sqrt(2 * x_train)
Y_test = np.log10(x_test) + np.sin(x_test) + np.sqrt(x_test)

# train logistic regression for density ratio estimation
classifier = train_logistic_ratio_classifier(x_train.reshape(-1, 1), x_test.reshape(-1, 1))

# standard model
std_estimator = StandardEstimator(classifier=classifier)
std_estimator.fit(x_train, Y_train)
std_mse = std_estimator.evaluate(x_test, Y_test)

print(f"Standard Model MSE: {std_mse}")

# plotting
plt.figure(figsize=(10, 5))

# standard Model Loss
plt.plot(std_estimator.losses, label='Standard Model Loss', linestyle='-', color='blue')

# iterate over gamma values
for gamma in gamma_values:
    ru_estimator = RUEstimator(gamma=gamma, classifier=classifier)
    ru_estimator.fit(x_train, Y_train)
    ru_mse = ru_estimator.evaluate(x_test, Y_test)
    print(f"RU Model (Gamma={gamma}) MSE: {ru_mse}")
    plt.plot(ru_estimator.LOSS, label=f'RU Model Loss (Gamma={gamma})', linestyle='--')

plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.title('Model Training Loss Comparison')
plt.legend()
plt.show()
