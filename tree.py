import pandas as pd

# 真理値表を作成（真理値表の入力と出力）
data = {
    "a": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "b": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
    "c": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "d": [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    "F": [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

# データフレームに変換
df = pd.DataFrame(data)

# F=1の場合のインデックスを取得
ones = df[df["F"] == 1].index

# 組み合わせのリストを作成（F=1の行の組み合わせを積み合わせる）
terms = []
for i in ones:
    term = []
    for var in ["a", "b", "c", "d"]:
        if df[var][i] == 0:
            term.append(f"(1-{var})")
        else:
            term.append(var)
    terms.append(" * ".join(term))

# 各積項を加算して論理関数を生成
logical_function = " + ".join(terms)

# F= の形で表示
print(f"F = {logical_function}")

