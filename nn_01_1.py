import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# --- CPU実行の強制 ---
# TensorFlowのすべての操作をCPUに固定します。これによりGPU関連のエラーを回避します。
tf.config.set_visible_devices([], 'GPU')
# ----------------------

# パラメータ
time_steps = 5000
dt = 0.01  # 時間ステップ (ms)
V_rest = -65.0  # 静止膜電位 (mV)

# 神経細胞の状態 (float32 に統一)
V = np.float32(V_rest)  # 初期膜電位
n, m, h = np.float32(0.0), np.float32(0.0), np.float32(0.0)  # ゲート変数

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
        tf.keras.layers.Dense(1, input_shape=(1,), activation='relu', dtype=tf.float32) 
    ])
    # KerasのEager実行を無効化 (安定したグラフモード)
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

# シミュレーションのステップごとに計算する関数
def run_simulation():
    global V, n, m, h
    
    # 状態変数をリセット
    V = np.float32(V_rest)
    n, m, h = np.float32(0.0), np.float32(0.0), np.float32(0.0)
    
    # 時間配列も float32 に
    time = np.arange(0, time_steps * dt, dt, dtype=np.float32)
    membrane_potential = np.zeros(time_steps, dtype=np.float32)
    
    # シミュレーション実行
    for i in range(time_steps):
        # ホジキン・ハクスリー方程式
        I_Na = 120.0 * (m ** 3) * h * (V - 50.0)
        I_K = 36.0 * (n ** 4) * (V + 77.0)
        I_L = 0.3 * (V + 54.387)
        
        # 総電流
        I_total = I_Na + I_K + I_L
        
        # 微分方程式の計算 (Euler法)
        dV = (0.0 - I_total) / 1.0 
        V += dV * dt
        
        # ゲート変数の更新 (Euler法)
        dn = alpha_n(V) * (1.0 - n) - beta_n(V) * n
        dm = alpha_m(V) * (1.0 - m) - beta_m(V) * m
        dh = alpha_h(V) * (1.0 - h) - beta_h(V) * h
        
        n += dn * dt
        m += dm * dt
        h += dh * dt
        
        membrane_potential[i] = V
        
        # シミュレーションの途中で発散していないかチェック
        if np.isnan(V) or np.isinf(V):
            print(f"警告: 膜電位がステップ {i} ({time[i]:.2f} ms) で発散しました。")
            return time[:i], membrane_potential[:i]
            
    return time, membrane_potential

# ----------------------------------------------------------------------
# メイン処理
# ----------------------------------------------------------------------

# シミュレーション結果を取得
time, membrane_potential = run_simulation()

# データが空でないかチェック
if len(time) == 0:
    print("致命的なエラー: データが初期段階で不安定になりました。シミュレーションパラメータ (dtなど) を見直してください。")
    exit()

print(f"最終的に学習に使用するデータ長: {len(time)} ステップ ({time[-1]:.2f} ms)")

# ニューラルネットワークでのフィードバック
model = simple_neural_network(time)

# モデルの学習 (CPU固定で実行)
try:
    # 入力 (time) を (N, 1) の形状にする
    model.fit(time.reshape(-1, 1), membrane_potential, epochs=50, verbose=0)
    print("Keras学習に成功しました。")
except Exception as e:
    print("\n--- 致命的な Keras 学習エラー ---")
    print("CPU固定モードでエラーが発生しました。データ型または環境設定に重大な問題がある可能性があります。")
    print("元のエラー:", e)
    exit()

# ネットワークからの予測をプロット
predicted_potential = model.predict(time.reshape(-1, 1)).flatten()

# 結果を表示
plt.figure(figsize=(10, 6))
plt.plot(time, membrane_potential, label='Hodgkin-Huxley Model (Target)', color='blue')
plt.plot(time, predicted_potential, label='Neural Network Prediction', linestyle='--', color='red')
plt.title('Comparison of Hodgkin-Huxley Model and Neural Network Prediction')
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.legend()
plt.grid(True)
plt.show()