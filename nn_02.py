import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# シンプルなニューラルネットワークモデル
model = tf.keras.Sequential([
    layers.Dense(10, activation='relu', input_shape=(1,)),  # 1つの入力ニューロン
    layers.Dense(1)  # 出力層（ニューロン2の状態）
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='mean_squared_error')

# 入力データとターゲットデータの準備（シンプルなデータで例）
input_data = np.linspace(-1, 1, 1000).reshape(-1, 1)  # ニューロン1の入力
target_data = 0.5 * input_data  # ニューロン2のターゲット（簡単な線形関係）

# 学習
model.fit(input_data, target_data, epochs=100)

# 出力の予測
predictions = model.predict(input_data)

# 結果のプロット
plt.plot(input_data, target_data, label="Target (Neuron 2)")
plt.plot(input_data, predictions, label="Predicted (Neuron 2)")
plt.xlabel('Input')
plt.ylabel('Output')
plt.legend()
plt.show()

