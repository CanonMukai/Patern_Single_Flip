#-*- coding:utf-8 -*-

#######################################
# パターン形成
# 方法: Single_Flip
#######################################
#
# 必要なライブラリの読み込み
#
import numpy as np
import math
import matplotlib.pyplot as plt

#
# 基本的なパラメタ
#
# 一辺あたりの格子点の個数
L = 50
# 全ての格子点の個数
N = L*L
# β = 1 / (kB*T)
beta = 0.3

#
# シミュレーテッド・アニーリングのパラメタ
#
# 探索回数 (整数)
n_itrn = 10000


# スピンiをひっくり返したときのエネルギー計算 and 状態更新
def single_flip(i):
    ix = i % L
    iy = int(i / L)
    de = 0
    # 左のスピン
    if ix != 0:
        de += stat[(ix-1) + iy*L]
    else:
        de += stat[(L-1) + iy*L]
    # 下のスピン
    if iy != 0:
        de += stat[ix + (iy-1)*L]
    else:
        de += stat[ix + (L-1)*L]
    # 右のスピン
    if ix != L-1:
        de += stat[(ix+1) + iy*L]
    else:
        de += stat[0 + iy*L]
    # 上のスピン
    if iy != L-1:
        de += stat[ix + (iy+1)*L]
    else:
        de += stat[ix + 0*L]

    de = de * 2 * stat[i]  # ΔE
    # 状態遷移 W
    if de < 0 and math.exp(-beta * float(de)) > np.random.rand():
        stat[i] = -stat[i]

#
# 初期設定
#
# ランダムに白黒にする: 0 or 1 を N個
stat = np.random.randint(0, 2, N) # 状態の設定
stat_memo = stat
stat = 2*stat - 1                 # 0 → -1,  1 → 1  0:黒 1:白
stat_int = np.array(stat)         # 状態のコピー
# 状態のリスト
stat_list = []
stat_list.append(np.reshape(stat_memo, (L, L)))

#
# --- ループ開始 ---
#
for it in range(1, n_itrn+1):
    i = np.random.randint(N)
    single_flip(i)

    # 状態の保存
    if it % 1000 == 0:
        stat1 = (stat + 1) / 2
        stat2 = np.reshape(stat1, (L, L))
        stat_list.append(stat2)
#
# --- ループ終了 ---
#


#
# --- 画像の出力 ---
#
fig = plt.figure(figsize=(15, 10))

count = 0
for stat1 in stat_list:
    ax = fig.add_subplot(2, 6, count+1)
    ax.imshow(stat1, cmap=plt.cm.gray, interpolation='nearest')
    it = count*1000
    ax.set_title('loop:%d' % it)
    count += 1
plt.show()
