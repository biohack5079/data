import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# パラメータ
time_steps = 5000
dt = 0.01  # 時間ステップ (ms)
V_rest = -65.0  # 静止膜電位 (mV)

# 神経細胞の状態
V = V_rest  # 初期膜電位
n, m, h = 0.0, 0.0, 0.0  # ゲート変数

# ゲート関数
def alpha_n(V): return 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
def beta_n(V): return 0.125 * np.exp(-(V + 65) / 80)
def alpha_m(V): return 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
def beta_m(V): return 4 * np.exp(-(V + 65) / 18)
def alpha_h(V): return 0.07 * np.exp(-(V + 65) / 20)
def beta_h(V): return 1 / (1 + np.exp(-(V + 35) / 10))

# 簡単なニューラルネットワーク (1層)
def simple_neural_network(inputs):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1, input_dim=1, activation='relu')  # 1層のパーセプトロン
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# シミュレーションのステップごとに計算する関数
def run_simulation():
    global V, n, m, h
    
    time = np.arange(0, time_steps * dt, dt)
    membrane_potential = np.zeros(time_steps)
    
    # シミュレーション実行
    for i in range(time_steps):
        I_Na = 120 * (m ** 3) * h * (V - 50)  # ナトリウム電流
        I_K = 36 * (n ** 4) * (V + 77)  # カリウム電流
        I_L = 0.3 * (V + 54.387)  # 漏れ電流
        
        # 総電流
        I_total = I_Na + I_K + I_L
        
        # 微分方程式の計算 (Euler法)
        dV = (0 - I_total) / 1.0  # 外部刺激なし
        V += dV * dt
        
        # ゲート変数の更新 (Euler法)
        dn = alpha_n(V) * (1 - n) - beta_n(V) * n
        dm = alpha_m(V) * (1 - m) - beta_m(V) * m
        dh = alpha_h(V) * (1 - h) - beta_h(V) * h
        
        n += dn * dt
        m += dm * dt
        h += dh * dt
        
        membrane_potential[i] = V
    
    return time, membrane_potential

# シミュレーション結果
time, membrane_potential = run_simulation()

# ニューラルネットワークでのフィードバック（シンプルなパーセプトロン）
model = simple_neural_network(time)
model.fit(time.reshape(-1, 1), membrane_potential, epochs=50, verbose=0)

# ネットワークからの予測をプロット
predicted_potential = model.predict(time.reshape(-1, 1))

# 結果を表示
plt.plot(time, membrane_potential, label='Hodgkin-Huxley Model')
plt.plot(time, predicted_potential, label='Neural Network Prediction', linestyle='dashed')
plt.title('Comparison of Hodgkin-Huxley Model and Neural Network Prediction')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.legend()
plt.grid(True)
plt.show()

