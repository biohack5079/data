#include "module.h"
#include "local_learning_synapse.h"
#include "model_manager.h"

namespace nest_module {

/**
 * @brief NESTカーネルにカスタムモジュールを登録するためのクラス。
 * * このモジュールは、非誤差逆伝播（non-BP）の局所学習SNN用のカスタムシナプスを登録します。
 */
class Module : public nest::Module
{
public:
    Module()
    {
        // CMakeLists.txtで定義したライブラリ名と一致させる
        set_module_name("nest_module");
        set_module_description("Custom module for non-BP local learning SNN.");

        // モデルマネージャーを取得し、新しいシナプスモデルを登録
        nest::ModelManager::instance()
            // 💡 Pythonから参照する名前: 'local_learning_synapse'
            .register_synapse_model<LocalLearningSynapse>("local_learning_synapse");
    }
};

} // namespace nest_module

// NESTがモジュールをロードするための必須マクロ。
// モジュールクラスをNESTカーネルに登録します。
NEST_REGISTER_MODULE(nest_module::Module)