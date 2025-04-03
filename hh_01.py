import numpy as np
import matplotlib.pyplot as plt

# 定数
C_m = 1.0  # 細胞膜の容量 (μF/cm^2)
g_Na = 120.0  # ナトリウムチャネルの最大伝導度 (mS/cm^2)
g_K = 36.0  # カリウムチャネルの最大伝導度 (mS/cm^2)
g_L = 0.3  # 漏れチャネルの最大伝導度 (mS/cm^2)
E_Na = 50.0  # ナトリウムの平衡電位 (mV)
E_K = -77.0  # カリウムの平衡電位 (mV)
E_L = -54.387  # 漏れイオンの平衡電位 (mV)

# 関数定義: 関数a、b、n、m、hはHHモデルの動的なゲート変数に関する式
def alpha_n(V):
    return (0.01 * (V + 55)) / (1 - np.exp(-(V + 55) / 10))

def beta_n(V):
    return 0.125 * np.exp(-(V + 65) / 80)

def alpha_m(V):
    return (0.1 * (V + 40)) / (1 - np.exp(-(V + 40) / 10))

def beta_m(V):
    return 4.0 * np.exp(-(V + 65) / 18)

def alpha_h(V):
    return 0.07 * np.exp(-(V + 65) / 20)

def beta_h(V):
    return 1.0 / (1 + np.exp(-(V + 35) / 10))

# HHモデルの数値積分のメインコード
def simulate_hh(T=50, dt=0.01):
    # 時間軸の作成
    time = np.arange(0, T, dt)
    num_steps = len(time)
    
    # 初期条件
    V = -65.0  # 初期膜電位 (mV)
    n = alpha_n(V) / (alpha_n(V) + beta_n(V))  # 初期のnの値
    m = alpha_m(V) / (alpha_m(V) + beta_m(V))  # 初期のmの値
    h = alpha_h(V) / (alpha_h(V) + beta_h(V))  # 初期のhの値
    
    # 結果保存用配列
    V_vals = np.zeros(num_steps)
    
    # シミュレーション開始
    for i in range(num_steps):
        # 電位更新
        I_Na = g_Na * (m ** 3) * h * (V - E_Na)  # ナトリウム電流
        I_K = g_K * (n ** 4) * (V - E_K)  # カリウム電流
        I_L = g_L * (V - E_L)  # 漏れ電流
        I_total = I_Na + I_K + I_L  # 総電流
        
        # ガウス白色雑音などの外部刺激を加えることも可能です
        # 例: I_ext = np.random.normal(0, 0.5)  # 外部刺激 (μA/cm^2)
        I_ext = 0.0  # 外部刺激なし
        
        # 微分方程式の計算 (Euler法)
        dV = (I_ext - I_total) / C_m  # 電位の変化
        V += dV * dt
        
        # ゲート変数の更新 (Euler法)
        dn = alpha_n(V) * (1 - n) - beta_n(V) * n
        dm = alpha_m(V) * (1 - m) - beta_m(V) * m
        dh = alpha_h(V) * (1 - h) - beta_h(V) * h
        
        n += dn * dt
        m += dm * dt
        h += dh * dt
        
        # 記録
        V_vals[i] = V
    
    return time, V_vals

# シミュレーション実行
time, V_vals = simulate_hh()

# 結果をプロット
plt.plot(time, V_vals)
plt.title('Hodgkin-Huxley Model: Membrane Potential vs Time')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.grid(True)
plt.show()

