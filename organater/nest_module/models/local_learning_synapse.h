#ifndef LOCAL_LEARNING_SYNAPSE_H
#define LOCAL_LEARNING_SYNAPSE_H

// 最終修正 V6: nest/ プレフィックスを削除し、
// CMakeLists.txt で指定したソースディレクトリのパスに合わせます。

#include <models/static_synapse.h>
#include <lib/models/default_properties.h>
#include <lib/models/connector_model.h>

namespace nest_module {

// Atomic weight states
enum class SynapticState {
    NONE = 0,
    WEAK_INH = -1,
    STRONG_INH = -2,
    WEAK_EXC = 1,
    STRONG_EXC = 2
};

// StaticSynapseをベースに、最小限の可塑的要素を追加
class LocalLearningSynapse : public nest::StaticSynapse<LocalLearningSynapse>
{
public:
    // Synapse properties (parameters)
    struct Properties : nest::DefaultProperties
    {
        double eta; // Base step size for discrete weight change
        
        // Actual weight values mapped from discrete states
        double weight_exc_weak;
        double weight_exc_strong;
        double weight_inh_weak;
        double weight_inh_strong;

        double min_w; 
        double max_w; 
    };

    LocalLearningSynapse();

    // Set parameters
    void set_properties(const Properties& p);
    
    // Handle spike from presynaptic neuron (where learning logic executes)
    void hit_presynaptic(
        nest::double_t, 
        nest::double_t, 
        const nest::Spike&, 
        nest::Connection*
    );
    
private:
    Properties p_;
    
    // Discrete weight state replaces continuous weight 'w_'
    SynapticState w_state_; 
    
    // Helper function: Converts discrete state to NEST's required double weight
    nest::double_t state_to_weight(SynapticState state) const;

    // // Placeholder for local error signal state (e.g., last error time)
    // // nest::double_t last_error_signal_time_; 
};

} // namespace nest_module

#endif // LOCAL_LEARNING_SYNAPSE_H