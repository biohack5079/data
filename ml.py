import torch
import torch.nn as nn
import torch.optim as optim

# 真理値表のデータ
data = [
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 1, 0, 0, 1],
    [0, 1, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
]

# データをテンソルに変換
data = torch.tensor(data, dtype=torch.float32)
X = data[:, :-1]  # 入力 (a, b, c, d)
y = data[:, -1:]  # 出力 (F)

# シンプルな線形モデル（活性化関数なし）
class LinearModel(nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.fc = nn.Linear(4, 1, bias=True)  # 1層の線形変換
    
    def forward(self, x):
        return self.fc(x)  # 活性化関数なし

# モデル、損失関数、最適化関数の設定
model = LinearModel()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 学習
epochs = 1000
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()

# 学習した重みを取得
W = model.fc.weight.detach().numpy()
b = model.fc.bias.detach().numpy()

# 数式の生成
equation = f"F(a, b, c, d) = {W[0,0]:.3f} * a + {W[0,1]:.3f} * b + {W[0,2]:.3f} * c + {W[0,3]:.3f} * d + {b[0]:.3f}"

print("\n学習した線形関数 F(a, b, c, d):")
print(equation)

