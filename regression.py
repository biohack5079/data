import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# 真理値表をデータフレームとして作成
data = {
    "a": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "b": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
    "c": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "d": [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    "F": [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

# データフレームに変換
df = pd.DataFrame(data)

# 説明変数を作成（各変数の積も含める）
df["ab"] = df["a"] * df["b"]
df["ac"] = df["a"] * df["c"]
df["ad"] = df["a"] * df["d"]
df["bc"] = df["b"] * df["c"]
df["bd"] = df["b"] * df["d"]
df["cd"] = df["c"] * df["d"]
df["abc"] = df["a"] * df["b"] * df["c"]
df["abd"] = df["a"] * df["b"] * df["d"]
df["acd"] = df["a"] * df["c"] * df["d"]
df["bcd"] = df["b"] * df["c"] * df["d"]
df["abcd"] = df["a"] * df["b"] * df["c"] * df["d"]

# 説明変数 X と目的変数 y
X = df.drop(columns="F")
y = df["F"]

# 重回帰分析を実行
model = LinearRegression()
model.fit(X, y)

# 重回帰分析の係数と切片を取得
coefficients = pd.Series(model.coef_, index=X.columns)
intercept = model.intercept_

# 結果の表示
print("Coefficients:")
print(coefficients)
print("\nIntercept:")
print(intercept)

# 関数 F の数式を組み立て
equation_terms = [f"{coeff} * {feature}" for coeff, feature in zip(coefficients, X.columns)]
equation = " + ".join(equation_terms)

# 最終的な数式
final_equation = f"F = {intercept} + " + equation
print("\n関数 F の数式:")
print(final_equation)

