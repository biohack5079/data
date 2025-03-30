import numpy as np
import matplotlib.pyplot as plt

# 関数を定義
def f1(x, y):
    return x * y

def f2(x, y):
    return 1 - x * y

def f3(x, y):
    return x + y - x * y

def f4(x, y):
    return 1 - x - y + x * y

def f5(x, y):
    return x + y - 2 * x * y

def f6(x, y):
    return 1 - x - y + 2 * x * y

# x と y の値のグリッドを作成
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
x, y = np.meshgrid(x, y)

# 各関数の z 値を計算
z1 = f1(x, y)
z2 = f2(x, y)
z3 = f3(x, y)
z4 = f4(x, y)
z5 = f5(x, y)
z6 = f6(x, y)

# サーフェスをプロット
fig = plt.figure(figsize=(18, 12))

ax1 = fig.add_subplot(231, projection='3d')
ax1.plot_surface(x, y, z1, cmap='viridis')
ax1.set_title('z = xy')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

ax2 = fig.add_subplot(232, projection='3d')
ax2.plot_surface(x, y, z2, cmap='viridis')
ax2.set_title('z = 1 - xy')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

ax3 = fig.add_subplot(233, projection='3d')
ax3.plot_surface(x, y, z3, cmap='viridis')
ax3.set_title('z = x + y - xy')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')

ax4 = fig.add_subplot(234, projection='3d')
ax4.plot_surface(x, y, z4, cmap='viridis')
ax4.set_title('z = 1 - x - y + xy')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')

ax5 = fig.add_subplot(235, projection='3d')
ax5.plot_surface(x, y, z5, cmap='viridis')
ax5.set_title('z = x + y - 2xy')
ax5.set_xlabel('X')
ax5.set_ylabel('Y')
ax5.set_zlabel('Z')

ax6 = fig.add_subplot(236, projection='3d')
ax6.plot_surface(x, y, z6, cmap='viridis')
ax6.set_title('z = 1 - x - y + 2xy')
ax6.set_xlabel('X')
ax6.set_ylabel('Y')
ax6.set_zlabel('Z')

# プロットを表示
plt.tight_layout()
plt.show()

