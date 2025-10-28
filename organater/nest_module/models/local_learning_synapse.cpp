#include "local_learning_synapse.h"
#include "connection.h"
#include <algorithm> // std::min, std::max のために必要

namespace nest_module {

LocalLearningSynapse::LocalLearningSynapse()
: w_(0.1) // 重みを初期化
{
    // パラメータのデフォルト値を設定
    p_.eta = 0.001;
    p_.min_w = 0.0;
    p_.max_w = 10.0;
}

void LocalLearningSynapse::set_properties(const Properties& p)
{
    p_ = p;
}

// 💡 最小限の学習則の骨格：重みを一定値で固定
void LocalLearningSynapse::hit_presynaptic(
    nest::double_t, 
    nest::double_t, 
    const nest::Spike&, 
    nest::Connection* connection)
{
    // ここに、BPを使わない「エラー率」と「前回入力」に基づく学習則ロジックを実装する
    
    // 例: 重みをランダムに変化させる（テスト用）
    // double delta_w = p_.eta * (static_cast<double>(rand()) / RAND_MAX - 0.5);
    // w_ += delta_w;
    
    // 💡 今回は、まずエラーを出さずにロードするために、重みをそのままに設定
    w_ = std::min(p_.max_w, std::max(p_.min_w, w_));
    
    connection->set_weight(w_);
}

} // namespace nest_module