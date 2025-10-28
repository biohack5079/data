#include "module.h"
#include "local_learning_synapse.h"
#include "model_manager.h"

namespace nest_module {

// 💡 CMakeLists.txtで定義した名前と同じクラス名
class Module : public nest::Module
{
public:
    Module()
    {
        set_module_name("nest_module");
        set_module_description("Custom module for non-BP local learning SNN.");

        // モデルマネージャーを取得し、新しいシナプスモデルを登録
        // 💡 Pythonから参照する名前: 'local_learning_synapse'
        nest::ModelManager::instance()
            .register_synapse_model<LocalLearningSynapse>("local_learning_synapse");
    }
};
} // namespace nest_module

// NESTがモジュールをロードするための必須マクロ
NEST_REGISTER_MODULE(nest_module::Module)