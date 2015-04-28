# -*- encoding: utf-8 -*-

#execfile('/Users/kohei/.pystartup')
import kfile
from defines import CH_SIM_TABLE_PATH

# 類似度テーブルを読み込む
CH_SIM_TABLE = kfile.load_data(CH_SIM_TABLE_PATH)

# 2つの文字の類似度を返す
def calc_sim_ch(a, b, use_table=1):
    if(use_table == 1):
        key = frozenset([a, b])
        if(key not in CH_SIM_TABLE):
            return 0.3
        return CH_SIM_TABLE[key]
    else:
        return 1 if a == b else 0

# 2つの文字列の類似度を返す
def calc_sim_text(X, Y, use_table=1):
    return float(calc_sim_text_n(X, Y, use_table)) / max(len(X), len(Y))

def calc_sim_text_n(X, Y, use_table=1):
    m = len(X)
    n = len(Y)
    L = [[0 for row in range(n+1)] for column in range(m+1)]

    for j in range(1, n + 1):
        for i in range(1, m + 1):
#            print i, j
            L[i][j] = max(
                    L[i][j-1],
                    L[i-1][j],
                    L[i-1][j-1] + calc_sim_ch(X[i-1], Y[j-1], use_table)
                    )
    return L[m][n]

# 20000回の演算で5秒弱?
# 問題にも索引をつける必要がありそう

#print "start"
#X = u"ab"
#Y = u"ac"
#print calc_sim_text(X, Y, 0)



