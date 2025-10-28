# organater/python_scripts/network.py

import nest

def create_network():
    """
    ニューロンネットワークを作成し、カスタムシナプスモデルで接続します。
    ここでは、単純な3層構造（入力、中間、出力）を想定します。
    """
    
    # ----------------------------------------------------
    # 1. ニューロンの作成
    # ----------------------------------------------------
    
    # 生物学的妥当性を考慮し、HHモデルを使用（ただし計算負荷に注意）
    input_size = 3    # 例: XORゲートの入力や単純な刺激
    hidden_size = 5   # 中間層（学習を行う単体ニューロンの代わり）
    output_size = 2   # 出力層（例: 応答、エラー信号を受け取る場所）

    # ニューロンモデルの選択: LFPモデルの hh_psc_alpha を使用
    input_neurons = nest.Create("hh_psc_alpha", input_size)
    hidden_neurons = nest.Create("hh_psc_alpha", hidden_size)
    output_neurons = nest.Create("hh_psc_alpha", output_size)

    # ----------------------------------------------------
    # 2. カスタムシナプスモデルのパラメータ設定
    # ----------------------------------------------------
    
    # 💡 C++で定義したカスタムシナプスモデルのパラメータを設定
    syn_spec_local_learning = {
        "model": "local_learning_synapse",  # 💡 nest_module/module.cpp で登録した名前
        "weight": 5.0,                      # 初期シナプス重み
        "delay": 1.0,                       # シナプス遅延 (ms)
        "eta": 0.001,                       # C++で定義した学習率 (learning_rate)
        "min_w": 0.0,                       # 最小重み
        "max_w": 10.0                       # 最大重み
        # 💡 その他、エラー信号伝達に必要なカスタムパラメータを追加
    }

    # ----------------------------------------------------
    # 3. ネットワークの接続
    # ----------------------------------------------------

    # ① 入力層 -> 中間層の接続（カスタム学習）
    # この接続で、誤差逆伝播を使わない局所的な学習が行われます。
    nest.Connect(
        input_neurons, 
        hidden_neurons, 
        syn_spec=syn_spec_local_learning
    )
    
    # ② 中間層 -> 出力層の接続（静的または別の学習則）
    # 簡単のため、静的（学習なし）なシナプスで接続
    nest.Connect(
        hidden_neurons, 
        output_neurons, 
        syn_spec={"model": "static_synapse", "weight": 2.0}
    )

    # ③ 出力層 -> 入力/中間層へのフィードバック接続（学習に必要なエラー信号の伝達）
    # 💡 ご提示のアルゴリズムの「エラー率」を伝達するための重要な回路
    # C++のシナプスモデルがこのフィードバック信号を受け取って重みを更新するロジックが必要です。
    nest.Connect(
        output_neurons, 
        hidden_neurons, 
        syn_spec={"model": "static_synapse", "weight": -1.0} # 例: 抑制性フィードバック
    )

    # 全てのニューロンをまとめて返す（recorder.pyなどで使用するため）
    all_neurons = list(input_neurons) + list(hidden_neurons) + list(output_neurons)
    return all_neurons