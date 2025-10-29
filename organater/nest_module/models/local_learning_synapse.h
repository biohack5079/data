#ifndef LOCAL_LEARNING_SYNAPSE_H
#define LOCAL_LEARNING_SYNAPSE_H

// 🚨 最終修正: static_synapse.h を継承元にし、パスを見つけやすいように修正。
// static_synapse.h は models/ 直下に、その他は lib/models/ にある可能性を考慮したハイブリッド型です。

// static_synapse.h は models/ 直下に存在すると仮定
#include <models/static_synapse.h>   // ⬅️ static_synapse.h を使用

// default_properties.h と connector_model.h は lib/models/ に存在すると仮定
#include <lib/models/default_properties.h>     
#include <lib/models/connector_model.h>        

namespace nest_module {

// 💡 原子的な重み状態を定義
// ノイズ耐性のために、重みを限られた離散的なレベルに量子化
enum class SynapticState {
    NONE = 0,        // 接続なし
    WEAK_INH = -1,   // 弱結合 (抑制性)
    STRONG_INH = -2, // 強結合 (抑制性)
    WEAK_EXC = 1,    // 弱結合 (興奮性)
    STRONG_EXC = 2   // 強結合 (興奮性)
};

// StaticSynapseをベースに、最小限の可塑的要素を追加
class LocalLearningSynapse : public nest::StaticSynapse<LocalLearningSynapse> // ⬅️ 継承元を StaticSynapse に変更
{
public:
    // シナプスで保持するプロパティ（パラメータ）
    // nest::DefaultPropertiesを継承しています
    struct Properties : nest::DefaultProperties
    {
        // 💡 連続的な学習率 'eta' は離散的な更新量の基数として保持
        double eta;      // 学習の基本量/離散的な重み変化のステップサイズ
        
        // 💡 離散的な状態を浮動小数点値にマッピングするための実際の重み値
        // これらはPythonから設定可能
        double weight_exc_weak;
        double weight_exc_strong;
        double weight_inh_weak;
        double weight_inh_strong;

        // 重み値のクリッピングは不要だが、慣例として保持
        double min_w;    
        double max_w;    
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
    
    // 💡 連続的な重み 'w_' を廃止し、離散的な状態 'w_state_' を使用
    SynapticState w_state_; 
    
    // 💡 補助関数: 離散的な状態をNESTが要求する浮動小数点重みに変換
    nest::double_t state_to_weight(SynapticState state) const;

    // 💡 [重要] エラー信号の局所的な状態を保持するための変数
    // 例: 前回、後シナプスからエラー信号が来た時刻やフラグ
    // nest::double_t last_error_signal_time_; 
};

} // namespace nest_module

#endif // LOCAL_LEARNING_SYNAPSE_H