# organater/nest_module/CMakeLists.txt (最終ビルド成功を目指す版 V8)

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
include_directories(
  SYSTEM
  ${NEST_INSTALL_PREFIX}/include/nest  # 1. インストールされたNESTのヘッダー
  
  # 💡 NESTのソースヘッダーへの最終調整パス (V8: 全てを含める)
  ${NEST_SOURCE_DIR}                   # 2. ソースルート (lib/ や models/ の親)
  ${NEST_SOURCE_DIR}/lib               # 3. <lib/...> を解決するため
  ${NEST_SOURCE_DIR}/models            # 4. ⬅️ <models/...> を解決するため
  ${NEST_SOURCE_DIR}/nestkernel        # 5. nestkernel内のコアヘッダーを網羅
  
  # 💡 カスタムモジュールのヘッダーへのパス
  ${MODULE_ROOT_DIR}                   # module.h があるパス
  ${MODULE_ROOT_DIR}/models            # local_learning_synapse.h があるパス
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

# 共有ライブラリのrpathを設定
set_target_properties(nest_module PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "${NEST_INSTALL_PREFIX}/lib/nest"
    INSTALL_RPATH_USE_ORIGIN TRUE
    SKIP_INSTALL_RPATH FALSE
)