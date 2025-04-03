import numpy as np
import matplotlib.pyplot as plt

# HHモデルのパラメータ
C = 1.0  # 膜容量
g_Na = 120  # Naチャネルの最大導電率
g_K = 36  # Kチャネルの最大導電率
g_L = 0.3  # 漏れチャネルの導電率
E_Na = 50  # Naの平衡電位
E_K = -77  # Kの平衡電位
E_L = -54.4  # 漏れチャネルの平衡電位

# HHモデルの方程式
def hh_model(V, m, h, n, I):
    dV = (I - g_Na*m**3*h*(V - E_Na) - g_K*n**4*(V - E_K) - g_L*(V - E_L)) / C
    dm = 0.1*(25 - V) / (np.exp((25 - V)/10) - 1) * (1 - m) - 4 * np.exp(-V/18) * m
    dh = 0.07 * np.exp(-V/20) * (1 - h) - h / (np.exp((30 - V)/10) + 1)
    dn = 0.1*(10 - V) / (np.exp((10 - V)/10) - 1) * (1 - n) - 0.125 * np.exp(-V/80) * n
    return dV, dm, dh, dn

# 初期条件とシナプス効果
V1 = -65  # 初期膜電位1
V2 = -65  # 初期膜電位2
m1, h1, n1 = 0.05, 0.6, 0.32  # 初期のm, h, n
m2, h2, n2 = 0.05, 0.6, 0.32  # 初期のm, h, n
I1, I2 = 10, 0  # 初期の入力電流

time = np.linspace(0, 100, 1000)
V1_trace = []
V2_trace = []

for t in time:
    # 細胞1の膜電位を更新
    dV1, dm1, dh1, dn1 = hh_model(V1, m1, h1, n1, I1)
    V1 += dV1
    m1 += dm1
    h1 += dh1
    n1 += dn1
    V1_trace.append(V1)

    # 細胞2の膜電位を更新（細胞1の膜電位の影響）
    I2 = 0.5 * (V1 - V2)  # シナプス効果
    dV2, dm2, dh2, dn2 = hh_model(V2, m2, h2, n2, I2)
    V2 += dV2
    m2 += dm2
    h2 += dh2
    n2 += dn2
    V2_trace.append(V2)

plt.plot(time, V1_trace, label="Cell 1")
plt.plot(time, V2_trace, label="Cell 2")
plt.xlabel('Time')
plt.ylabel('Membrane Potential (mV)')
plt.legend()
plt.show()

