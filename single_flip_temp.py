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
l = 20
# 全ての格子点の個数
n = l*l
# 辺の数
m = 2*n

#
# シミュレーテッド・アニーリングのパラメタ
#
# 初期温度 (実数)
T_ini = 1000.0  
# 温度減少率 (実数 < 1.0)
alpha = 0.1      
# 探索回数 (整数)
n_itrn = 10000
# 温度変更の間隔 (整数 < n_itrn)
T_intv = 100    
# 状態更新がなかった時のエネルギー増分 (整数)
dE = 1

#
# 辺のリスト読み込み
#

edge = np.array([0, 1])
edge = np.array([edge, (0, l)])
for i in range(1, n):
    if (i % l) == (l-1):
        edge = np.insert(edge, 2*i, [i, i-l+1], axis=0)
    else:
        edge = np.insert(edge, 2*i, [i, i+1], axis=0)
        
    if i >= l*(l-1):
        edge = np.insert(edge, 2*i+1, [i, i%l], axis=0)
    else:
        edge = np.insert(edge, 2*i+1, [i, i+l], axis=0)

        
#
# 関数: エネルギー
#
def energy(s):
    H = 0
    for k in range(m):
        i = edge[k][0]
        j = edge[k][1]  # 隣り合う格子点 i, j に対して
        H += s[i]*s[j]  # H = Σ s_i s_j
    return -H  # 隣り合う格子点が同じ色のときにHが小さくなるように

#
# 初期設定 
#
# ランダムに組分けする: 0 or 1 を n個
stat = np.random.randint(0, 2, n) # 状態(組分け情報)の設定
stat_memo = stat
stat = 2*stat - 1                 # 0 → -1,  1 → 1  0:黒 1:白
stat_int = np.array(stat)         # 状態のコピー
# 初期温度
T = T_ini
# 初期エネルギー
E_old = energy(stat)
# 最低エネルギー
E0 = -2*n  # 辺の数
# 状態のリスト
stat_list = []
#stat_list.append(np.reshape(stat_memo, (l, l)))

# --- ループ開始 ---
#
for i in range(10):
    T_ini -= 100 * i
    
    for it in range(1, n_itrn+1): 
        
        # どれか格子点１つランダムに選ぶ
        k = np.random.randint(n)  # kが選ばれた
        
        # kの白黒を変更: 中間状態を更新
        stat_int[k] = -stat[k]    # 符号を反転：kの色のみを変更
        
        # 遷移確率pを計算
        E_int = energy(stat_int)
        dH = float(E_int - E_old)
        p = math.exp( -dH / T )
        
        # 状態更新: エネルギー降下 or 上昇でもある割合で...
        if np.random.rand() < p:
            stat[k] = stat_int[k]  # 中間状態を新しい状態として採用
            E_old = E_int          # エネルギーも更新
        else:
            stat_int[k] = stat[k]  # 採用しない場合は元に戻す
            E_old += dE            # 状態更新なしでエネルギー増加
            
        # エネルギーが最低エネルギーE0になったらループを抜ける
        if E_old == E0:
            break

        # 温度の更新 (T_intv = 100毎、と言うことは100回温度を下げる)
        #if (it + 1) % T_intv == 0: 
        #   T *= 1.0 - alpha        

    stat1 = (stat + 1) / 2
    stat2 = np.reshape(stat1, (l, l))
    stat_list.append(stat2)
#
# --- ループ終了 ---
#

fig = plt.figure(figsize=(15, 10))


count = 0
temp_memo = 1000
for stat1 in stat_list:
    ax = fig.add_subplot(2, 5, count+1)
    ax.imshow(stat1, cmap=plt.cm.gray, interpolation='nearest')
    temp = temp_memo - 100 * count
    ax.set_title('temp:%d' % temp)
    count += 1
plt.show()

#
# ターミナルへの出力
#
gr0 = []
gr1 = []
for i in range(n):
    if stat[i] == 1:  # 白
        gr0.append(i)
    else:             # 黒
        gr1.append(i)

print('白の格子点: %s' % gr0)
print('黒の格子点: %s' % gr1)
print('不満足数: %d' % int((energy(stat) - E0)/2))



