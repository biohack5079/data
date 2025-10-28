# organater/python_scripts/simulation.py

import nest
import os
import sys

# 💡 内部モジュールをインポートするために、カレントディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

from network import create_network
from stimuli import create_stimuli
from recorder import setup_recorders
from utils import log

# 💡 カスタムC++モジュールをロードする関数
def install_custom_module():
    """カスタムNESTモジュール（nest_module）をロードします。"""
    try:
        # 💡 CMakeLists.txtで定義したモジュール名を使用
        nest.Install('nest_module') 
        log("Custom NEST module 'nest_module' installed successfully.")
        return True
        
    # 💡 修正点: nest.exceptions.NESTError の代わりに汎用的な Exception を使用
    except Exception as e: 
        # C++モジュールのロード失敗時に発生する可能性のあるエラーをキャッチ
        log(f"ERROR: Failed to install custom module 'nest_module'. Check C++ build/install steps and LD_LIBRARY_PATH. Error: {e}")
        return False

def run_simulation():
    # カーネルをリセットし、シミュレーションを開始
    nest.ResetKernel()
    log("Organater simulation started.")
    
    # 1. カスタムモジュールのロード
    if not install_custom_module():
        # モジュールロード失敗時は処理を中断
        log("Simulation aborted due to custom module installation failure.")
        return

    # 2. ネットワーク、刺激、レコーダーの作成
    # 💡 ここで network.py が実行され、カスタムシナプスが利用されます。
    neurons = create_network()
    stimuli = create_stimuli()
    recorders = setup_recorders()

    # 3. 接続処理（仮）
    # network.pyで作成された全てのニューロンを接続対象として使用
    
    # NEST Connectはデバイスとニューロン、ニューロンとニューロンを接続
    nest.Connect(stimuli, neurons)
    nest.Connect(neurons, recorders)

    # 4. シミュレーションの実行
    simulation_time = 1000.0  
    log(f"Simulating for {simulation_time} ms...")
    nest.Simulate(simulation_time)
    log("Simulation completed.")
    
    # 5. データ解析や保存処理（必要に応じて追加）
    # 例: recordersからデータを取得し、ファイルに書き出す処理

if __name__ == '__main__':
    run_simulation()