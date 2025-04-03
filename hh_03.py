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
V3 = -65  # 初期膜電位3
m1, h1, n1 = 0.05, 0.6, 0.32  # 初期のm, h, n
m2, h2, n2 = 0.05, 0.6, 0.32  # 初期のm, h, n
m3, h3, n3 = 0.05, 0.6, 0.32  # 初期のm, h, n
I1, I2, I3 = 10, 0, 0  # 初期の入力電流

time = np.linspace(0, 100, 1000)
V1_trace = []
V2_trace = []
V3_trace = []

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

    # 細胞3の膜電位を更新（細胞2の膜電位の影響）
    I3 = 0.5 * (V2 - V3)  # シナプス効果
    dV3, dm3, dh3, dn3 = hh_model(V3, m3, h3, n3, I3)
    V3 += dV3
    m3 += dm3
    h3 += dh3
    n3 += dn3
    V3_trace.append(V3)

# プロット
plt.plot(time, V1_trace, label="Cell 1 (HH)")
plt.plot(time, V2_trace, label="Cell 2 (HH)")
plt.plot(time, V3_trace, label="Cell 3 (HH)")
plt.xlabel('Time')
plt.ylabel('Membrane Potential (mV)')
plt.legend()
plt.title("HH Model with 3 Cells Interacting")
plt.show()

