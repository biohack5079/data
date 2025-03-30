import numpy as np
import matplotlib.pyplot as plt

# 関数 z = x + y - 2xy を定義
def f(x, y):
    return x + y - 2 * x * y

# x と y の値のグリッドを作成
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
x, y = np.meshgrid(x, y)

# z の値を計算
z = f(x, y)

# サーフェスをプロット
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')

# ラベルを設定
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# プロットを表示
plt.show()

