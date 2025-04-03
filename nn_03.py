import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# シンプルなニューラルネットワークモデル
model = tf.keras.Sequential([
    layers.Dense(10, activation='relu', input_shape=(1,)),  # 1つの入力ニューロン
    layers.Dense(1),  # 出力層（ニューロン2の状態）
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='mean_squared_error')

# 入力データとターゲットデータの準備（簡単なデータで例）
input_data = np.linspace(-1, 1, 1000).reshape(-1, 1)  # ニューロン1の入力
target_data_1 = 0.5 * input_data  # ニューロン2のターゲット（簡単な線形関係）
target_data_2 = 0.3 * input_data  # ニューロン3のターゲット

# 学習
model.fit(input_data, target_data_1, epochs=100)

# 出力の予測
predictions_1 = model.predict(input_data)

# 2番目のニューロンの学習
model.fit(input_data, target_data_2, epochs=100)

# 出力の予測
predictions_2 = model.predict(input_data)

# 3番目のニューロンの学習
target_data_3 = 0.2 * input_data  # 3番目のターゲット
model.fit(input_data, target_data_3, epochs=100)

# 出力の予測
predictions_3 = model.predict(input_data)

# 結果のプロット
plt.plot(input_data, target_data_1, label="Target Neuron 1 (NN)")
plt.plot(input_data, predictions_1, label="Predicted Neuron 1 (NN)")
plt.plot(input_data, target_data_2, label="Target Neuron 2 (NN)")
plt.plot(input_data, predictions_2, label="Predicted Neuron 2 (NN)")
plt.plot(input_data, target_data_3, label="Target Neuron 3 (NN)")
plt.plot(input_data, predictions_3, label="Predicted Neuron 3 (NN)")
plt.xlabel('Input')
plt.ylabel('Output')
plt.legend()
plt.title("NN Model with 3 Neurons Interacting")
plt.show()

