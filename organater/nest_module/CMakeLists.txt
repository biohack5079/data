cmake_minimum_required(VERSION 3.5)
project(nest_module CXX)

# =========================================================================
# 🚨 最終回避策の定義 (パスは固定)
# =========================================================================

# NESTのインストールパスを定義
set(NEST_INSTALL_PREFIX "/home/s24156/data/.venv")
set(NEST_SOURCE_DIR "/home/s24156/data/nest-simulator")
set(MODULE_ROOT_DIR "/home/s24156/data/organater/nest_module")

# -------------------------------------------------------------
# NESTのヘッダーとライブラリへの絶対パスを直接指定
# -------------------------------------------------------------

# ヘッダーファイルパスを設定
# 💡 V13: インクルードパスの完全網羅版
include_directories(
    SYSTEM
    ${NEST_INSTALL_PREFIX}/include
    ${NEST_SOURCE_DIR}                  
    ${NEST_SOURCE_DIR}/lib               
    ${NEST_SOURCE_DIR}/models            
    ${NEST_SOURCE_DIR}/nestkernel        
    ${NEST_SOURCE_DIR}/libnestutil                    
    
    # config.h のパス
    ${NEST_SOURCE_DIR}/build_shared_libs/libnestutil                    
    
    # name.h のパス
    ${NEST_SOURCE_DIR}/sli                             
    
    # 🚨 V13 最終修正: compose.hpp が存在するディレクトリを追加
    ${NEST_SOURCE_DIR}/thirdparty                      
    
    ${MODULE_ROOT_DIR}                   
    ${MODULE_ROOT_DIR}/models            
)

# 💡 共有モジュールライブラリの定義
add_library(nest_module MODULE
    module.cpp
    models/local_learning_synapse.cpp
)

# 必要なNESTライブラリへの絶対パスリンク (仮想環境内のファイル)
target_link_libraries(nest_module PUBLIC
    ${NEST_INSTALL_PREFIX}/lib/nest/libnestkernel.so
    ${NEST_INSTALL_PREFIX}/lib/nest/libmodels.so
    ${NEST_INSTALL_PREFIX}/lib/nest/libnest.so
)

# C++規格を指定
target_compile_features(nest_module PUBLIC cxx_std_17)

# 共有ライブラリのrpathを設定 (実行時にライブラリが見つかるように)
set_target_properties(nest_module PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "${NEST_INSTALL_PREFIX}/lib/nest"
    INSTALL_RPATH_USE_ORIGIN TRUE
    SKIP_INSTALL_RPATH FALSE
)

# インストールターゲットの定義
install(TARGETS nest_module
        DESTINATION "${NEST_INSTALL_PREFIX}/lib/nest"
)