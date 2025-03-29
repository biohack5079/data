import sympy as sp

# 変数の定義
z = sp.Symbol('z')

# 関数の定義
f = sp.exp(z) / (z - 1)**2

# 1. 関数を (z - 1) の形に変換
g = sp.exp(z).rewrite(sp.exp, exp=(z-1+1))  # exp(z) → exp(1) * exp(z-1)

# 2. exp(z-1) をマクローリン展開（z=1 の周り）
taylor_exp = sp.series(sp.exp(z-1), z-1, 0, 5).removeO()

# 3. 分母の (z - 1)^2 を展開に適用
expanded = (sp.exp(1) * taylor_exp) / (z - 1)**2

# 4. 各項を整理
laurent_series = sp.series(expanded, z, 1, n=5).removeO()

# **結果を表示**
print("元の関数: f(z) =", f)
print("\n1. 指数関数を変形: g(z) =", g)
print("\n2. exp(z-1) のテイラー展開:", taylor_exp)
print("\n3. (z-1)^2 で割る:", expanded)
print("\n4. ローラン展開の結果:", laurent_series)


