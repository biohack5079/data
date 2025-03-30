import numpy as np
import pandas as pd

def rss(y, t):
    return 0.5 * np.sum((y - t)**2) / y.shape[0]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

data = {
    "a": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "b": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
    "c": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "d": [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    "F": [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

x_train = df[["a", "b", "c", "d"]].values
t_train = df["F"].values.reshape(-1, 1)

np.random.seed(0)
w = np.random.randn(4, 1) * 0.1
b = np.zeros(1)

alpha = 0.1
epochs = 1000

for epoch in range(epochs):
    u = np.dot(x_train, w) + b
    y = sigmoid(u)
    loss = rss(y, t_train)
    delta = (y - t_train) * y * (1 - y)
    dw = np.dot(x_train.T, delta) / len(x_train)
    db = np.sum(delta) / len(x_train)
    w -= alpha * dw
    b -= alpha * db
    if epoch % 100 == 0:
        print(f"Epoch {epoch}: Loss = {loss}")

y_pred = sigmoid(np.dot(x_train, w) + b)
y_pred = (y_pred > 0.5).astype(int)
print("Predicted F:", y_pred.ravel())

print(f"F = {w[0,0]}*a + {w[1,0]}*b + {w[2,0]}*c + {w[3,0]}*d + {b[0]}")

