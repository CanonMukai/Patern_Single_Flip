#######################################
# 組分け
# 方法: シミュレーテッド・アニーリング
#######################################
#
# 必要なライブラリの読み込み
#
import numpy as np
import math

#
# 基本的なパラメタ
#
# 人数
n = 10
# 辺の数
m = 15 

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
edge = np.loadtxt('edge_group.txt', dtype='int')

#
# 関数: エネルギー
#
def energy(s):
    H = 0
    for k in range(m):
        i = edge[k][0]
        j = edge[k][1]  # 仲の悪い２人 i, j に対して
        H += s[i]*s[j]  # H = Σ s_i s_j
    return H

#
# 初期設定 
#
# ランダムに組分けする: 0 or 1 を n個
stat = np.random.randint(0, 2, n) # 状態(組分け情報)の設定
stat = 2*stat - 1                 # 0 → -1,  1 → 1 
stat_int = np.array(stat)         # 状態のコピー
# 初期温度
T = T_ini
# 初期エネルギー
E_old = energy(stat)
# 最低エネルギー
E0 = -m 

# --- ループ開始 ---
#
for it in range(n_itrn): 

    # だれか１人ランダムに選ぶ
    k = np.random.randint(n)  # kが選ばれた
    
    # kの組を変更: 中間状態を更新
    stat_int[k] = -stat[k]    # 符号を反転

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

    # 温度の更新 (T_intv毎)
    if (it + 1) % T_intv == 0:
        T *= 1.0 - alpha
#
# --- ループ終了 ---
#

#
# ターミナルへの出力
#
gr0 = []
gr1 = []
for i in range(n):
    if stat[i] == 1:
        gr0.append(i)
    else:
        gr1.append(i)
print('白組 ', gr0)
print('赤組 ', gr1)
print('不満足数: ', int((energy(stat) - E0)/2))
print('最終温度: ', T)

#
# ファイルへの出力
#
f = open('group.html','w')  # 出力ファイル
f.write('<!doctype html>\n<html lang ="ja">\n')
f.write(' <head>\n <meta charset="UTF-8">\n </head>\n <body>\n')
f.write(' <table border="1" cellspacing="0">\n')
f.write(' <tr><td colspan="2">敵対ペア</td><td>判定</td></tr>\n')
for k in range(m):
    i = edge[k][0]
    j = edge[k][1]
    if stat[i]*stat[j] > 0:
        st = '×'
    else:
        st = '◯'
    if stat[i] == 1:
        cl0 = '#ffffff'
    else:
        cl0 = '#ff3366'
    if stat[j] == 1:
        cl1 = '#ffffff'
    else:
        cl1 = '#ff3366'
    f.write(' <tr><td bgcolor="{}">{}</td><td bgcolor="{}">{}</td><td>{}</td></tr>\n'.format(cl0, i, cl1, j, st))
f.write(' </table>\n </body>\n</html>\n')
f.close()
