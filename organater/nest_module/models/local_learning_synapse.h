#ifndef LOCAL_LEARNING_SYNAPSE_H
#define LOCAL_LEARNING_SYNAPSE_H

#include "synapse_model.h"
#include "default_properties.h"
#include "connector_model.h"

namespace nest_module {

// StaticSynapseをベースに、最小限の可塑的要素を追加
class LocalLearningSynapse : public nest::SynapseModel<LocalLearningSynapse>
{
public:
    // シナプスで保持するプロパティ（パラメータ）
    struct Properties : nest::Default : Properties
    {
        // 💡 BPを使わない学習則のパラメータ
        double eta;       // 学習率 (learning_rate)
        double min_w;     // 最小重み
        double max_w;     // 最大重み
    };

    LocalLearningSynapse();

    // パラメータの設定
    void set_properties(const Properties& p);
    
    // スパイクが前シナプスにヒットしたときの処理（学習ロジックの実行場所）
    void hit_presynaptic(
        nest::double_t, 
        nest::double_t, 
        const nest::Spike&, 
        nest::Connection*
    );
    
private:
    Properties p_;
    nest::double_t w_; // シナプス重み
};

} // namespace nest_module

#endif // LOCAL_LEARNING_SYNAPSE_H