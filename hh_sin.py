import numpy as np
import matplotlib.pyplot as plt

# 関数の定義
def rss(y, t):
    return 0.5 * np.sum((y - t)**2) / y.shape[0]

def cross_entropy(y, t):
    return -np.sum(t * np.log(y + 1e-8)) / y.shape[0]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

class Sigmoid:
    def __init__(self, x):
        self.y = 1 / (1 + np.exp(-x))
        self.dy = (1 - self.y) * self.y

class Middle_layer:
    def __init__(self, n_upper, n, func):
        self.w = np.random.normal(0, 0.05, (n, n_upper + 1))
        self.w2 = np.delete(self.w, -1, 1)
        self.func = func

    def forward(self, y_in):
        dummy = np.ones((y_in.shape[0], 1))
        self.y_in = np.append(y_in, dummy, axis=1)
        self.u = np.dot(self.y_in, self.w.T)
        self.y_out = self.func(self.u).y

    def backward(self, y_b):
        self.delta = self.func(self.u).dy * y_b
        self.y_back = np.dot(self.delta, self.w2)
        self.w -= alpha * np.dot(self.delta.T, self.y_in)
        self.w2 = np.delete(self.w, -1, 1)

class Output_layer:
    def __init__(self, n_upper, n, c=False):
        self.w = np.random.normal(0, 0.05, (n, n_upper + 1))
        self.w2 = np.delete(self.w, -1, 1)
        self.c = c

    def activate(self, y_in, t):
        self.t = t
        dummy = np.ones((y_in.shape[0], 1))
        y_in = np.append(y_in, dummy, axis=1)
        u = np.dot(y_in, self.w.T)
        self.y_out = u
        if self.c:
            self.y_out = softmax(u)
        self.delta = self.y_out - self.t
        self.y_back = np.dot(self.delta, self.w2)
        self.w -= alpha * np.dot(self.delta.T, y_in)
        self.w2 = np.delete(self.w, -1, 1)

    def forward(self, y_in):
        dummy = np.ones((y_in.shape[0], 1))
        y_in = np.append(y_in, dummy, axis=1)
        u = np.dot(y_in, self.w.T)
        self.y_out = u
        if self.c:
            self.y_out = softmax(u)

# データの準備
x = np.linspace(0, 8, 129)
t = np.sin(x)
x2d = x[:, np.newaxis]
t2d = t[:, np.newaxis]

# 可視化
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax.set_xlabel("x", fontsize=15)
ax.set_ylabel("t", fontsize=15)
ax.set_xlim([0, 8])
ax.set_ylim([-1, 1])
ax.grid()
ax.plot(x, t, color="blue")
plt.show()

# モデルの設定
np.random.seed(10)
alpha = 0.25
epoch = 2000
interval = 100
y_r = []
epoch_r = []
nd = len(x)
idx = np.arange(nd)

# 中間層
mid_1 = Middle_layer(1, 3, Sigmoid)
mid_2 = Middle_layer(3, 3, Sigmoid)
out = Output_layer(3, 1)

# 学習関数
def train():
    for j in range(epoch):
        np.random.shuffle(idx)
        for k in idx:
            mid_1.forward(x2d[k:k + 1])
            mid_2.forward(mid_1.y_out)
            out.activate(mid_2.y_out, t2d[k:k + 1])
            mid_2.backward(out.y_back)
            mid_1.backward(mid_2.y_back)
        if j % interval == 0:
            mid_1.forward(x2d)
            mid_2.forward(mid_1.y_out)
            out.forward(mid_2.y_out)
            y_r.append(out.y_out)
            epoch_r.append(j)

# 学習の実行
train()

# 結果のプロット
fig, axs = plt.subplots(3, 2, sharey="all", figsize=(8, 15))
fig.subplots_adjust(hspace=0.3)

def plot_results():
    ct = 0
    for ax in axs.ravel():
        ct += 1
        ax.set_title(f"epoch : {epoch_r[ct]}", size=15)
        ax.set_xlabel("x", fontsize=15)
        if ct % 2 == 1:
            ax.set_ylabel("t", fontsize=15)
        ax.set_xlim([0, 8])
        ax.set_ylim([-1, 1])
        ax.grid()
        ax.plot(x, t, color="gray")
        ax.scatter(x2d, y_r[ct], marker="+", color="green")

plot_results()
plt.savefig("nn_model_epoch.png", bbox_inches="tight")
plt.show()

