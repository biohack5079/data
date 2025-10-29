#include "local_learning_synapse.h"
#include "connection.h"
#include <algorithm> // std::min, std::max のために必要
#include <cmath>     // std::abs のために必要

namespace nest_module {

// ----------------------------------------------------------------------
// 補助関数: 離散的な状態を浮動小数点重みに変換
// ----------------------------------------------------------------------
nest::double_t LocalLearningSynapse::state_to_weight(SynapticState state) const
{
    switch (state) {
        case SynapticState::NONE:
            return 0.0;
        case SynapticState::WEAK_EXC:
            return p_.weight_exc_weak;
        case SynapticState::STRONG_EXC:
            return p_.weight_exc_strong;
        case SynapticState::WEAK_INH:
            return p_.weight_inh_weak;
        case SynapticState::STRONG_INH:
            return p_.weight_inh_strong;
    }
    // 未定義の状態が来た場合のフォールバック（通常は発生しない）
    return 0.0; 
}


// ----------------------------------------------------------------------
// コンストラクタ
// ----------------------------------------------------------------------
LocalLearningSynapse::LocalLearningSynapse()
: w_state_(SynapticState::WEAK_EXC) // 💡 離散的な重み状態を初期化（例として弱興奮性）
{
    // 💡 パラメータのデフォルト値を設定
    p_.eta = 1.0; // 離散的な学習則では、etaはブール条件が満たされたときの「遷移の強さ」を示す定数
    p_.min_w = -10.0; // 連続的なクリッピングは行わないが、念のため保持
    p_.max_w = 10.0;
    
    // 💡 離散状態に対応する実際の重み値のデフォルト設定
    p_.weight_exc_weak = 0.5;
    p_.weight_exc_strong = 5.0;
    p_.weight_inh_weak = -0.5;
    p_.weight_inh_strong = -5.0;
}


// ----------------------------------------------------------------------
// プロパティ設定
// ----------------------------------------------------------------------
void LocalLearningSynapse::set_properties(const Properties& p)
{
    p_ = p;
    // 重み設定時、初期状態をデフォルトの興奮性弱結合にリセット
    // または、設定された重み値に近い状態に初期化するロジックをここに追加可能
}


// ----------------------------------------------------------------------
// スパイクヒット時の処理（学習則ロジック）
// ----------------------------------------------------------------------
void LocalLearningSynapse::hit_presynaptic(
    nest::double_t, 
    nest::double_t, 
    const nest::Spike&, 
    nest::Connection* connection)
{
    // 💡 興奮性の重み値を取得し、接続先に伝達
    // 興奮性か抑制性かを判定し、絶対値としてカーネルに重みを渡す。
    // w_state_がenumのため、state_to_weightを使ってdoubleに変換する必要がある。
    nest::double_t current_weight = state_to_weight(w_state_);
    connection->set_weight(current_weight);
    
    // ------------------------------------------------------------------
    // 💡 NANDベースの原子的な学習則の骨格 (状態遷移)
    // ------------------------------------------------------------------
    
    // TODO: 1. 後シナプスからエラー信号 E を取得するロジックを実装
    // bool E_is_present = get_error_signal_from_post_neuron(); 
    bool E_is_present = false; // 現状は仮のブール値
    
    // TODO: 2. 前回入力の有無 X を参照するロジックを実装
    bool X_is_present = true; // hit_presynapticが呼ばれた時点で前スパイクは来た(X=1)

    // 💡 NAND学習則の論理に基づいた原子的な状態遷移（例）
    if (X_is_present && E_is_present) {
        // 条件が満たされた場合、重み状態を離散的に遷移させる
        
        if (w_state_ == SynapticState::WEAK_EXC) {
            w_state_ = SynapticState::STRONG_EXC; // 弱興奮性 -> 強興奮性へジャンプ
        } 
        // 他の論理的条件（抑制、リセットなど）をここに追加

    } else {
        // エラーがない、または入力がない場合の処理（安定化、またはリセット）
        
        if (w_state_ == SynapticState::STRONG_EXC) {
            // w_state_ = SynapticState::WEAK_EXC; // 例: 強い状態を弱める
        }
    }
    
    // 💡 状態遷移後に新しい重みを設定し直す（状態が変わった場合のみ）
    connection->set_weight(state_to_weight(w_state_));

}

} // namespace nest_module