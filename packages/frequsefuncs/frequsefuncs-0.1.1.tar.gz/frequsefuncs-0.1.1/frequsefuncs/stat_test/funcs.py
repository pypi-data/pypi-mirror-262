



import scipy.stats

def thr_tscore_n_clvl(level):
    if level == 0.99:
        thr = 2.576
    elif level == 0.95:
        thr = 1.960
    elif level == 0.90:
        thr = 1.645
    elif level == 0.80:
        thr = 1.282
    elif level == 0.70:
        thr = 1.036
    elif level == 0.60:
        thr = 0.842
    else:
        thr = 1.960    #默认返回95%置信度
    return thr


def calcu_confidence_intv_rate(n1, n2, p1, p2, level):
    thr = thr_tscore_n_clvl(level)
    try:
        s1 = p1*(1-p1) / n1
        s2 = p2*(1-p2) / n2
        s = (s1+s2)**0.5
        d = p1 - p2
        z = abs(d) / s
        ci1 = d - thr*s
        ci2 = d + thr*s
        r_z = str(round(z,2))
        r_ci1 = str(round(ci1,4))
        r_ci2 = str(round(ci2,4))
        pval = str(round(scipy.stats.t.sf(abs(z), df = n1 + n2 - 2) * 2, 4))
    except:
        #print(s1, s2, s, d)
        raise
    if z > thr:
        txt = '显著'
    else:
        txt = '-'
    r = '@'.join([txt, pval, r_z, r_ci1, r_ci2])
    return r

def calcu_confidence_intv_value(n1, n2, m1, m2, v1, v2, level):
    try:
        thr = thr_tscore_n_clvl(level)
        s1 = v1 / n1
        s2 = v2 / n2
        s = (s1+s2)**0.5
        d = m1 - m2
        z = abs(d) / s
        ci1 = d - thr*s
        ci2 = d + thr*s
        r_z = str(round(z,4))
        r_ci1 = str(round(ci1,4))
        r_ci2 = str(round(ci2,4))
        pval = str(round(scipy.stats.t.sf(abs(z), df = n1 + n2 - 2) * 2, 4))
        if z > thr:
            txt = '显著'
        else:
            txt = '-'
        r = '@'.join([txt, pval, r_z, r_ci1, r_ci2])
    except:
        r = ''
    return r


def func_statistical_test(se, lst_col, flag, level):
    #print(type(se))
    #print(se)
    try:
        if flag == 'rate':
            n1 = se[lst_col[0]]
            n2 = se[lst_col[1]]
            p1 = se[lst_col[2]]
            p2 = se[lst_col[3]]
            if n1*n2*p1*p2*(1-p1)*(1-p2) > 0:
                r = calcu_confidence_intv_rate(n1, n2, p1, p2, level)
            else:
                r = '-'
        else:
            n1 = se[lst_col[0]]
            n2 = se[lst_col[1]]
            m1 = se[lst_col[2]]
            m2 = se[lst_col[3]]
            v1 = se[lst_col[4]]
            v2 = se[lst_col[5]]
            if n1*n2*m1*m2 > 0:
                r = calcu_confidence_intv_value(n1, n2, m1, m2, v1, v2, level)
            else:
                r = '-'
    except:
        #print(se, n1, n2, p1, p2)
        raise
    return r






############# 用来计算最小样本量 #############

def thr_tscore_n_power(power):
    if power == 0.90:
        thr = 1.28
    elif power == 0.80:
        thr = 0.84
    elif power == 0.70:
        thr = 0.52
    elif power == 0.60:
        thr = 0.25
    else:
        thr = 0.84    #默认返回80%统计功效
    return thr


#率值情况
def func_sample_size_rate(p1, p2, level, power):
    thr_lvl = thr_tscore_n_clvl(level)
    thr_pow = thr_tscore_n_power(power)
    a1 = float(p1-p2)**2
    a2 = float(p1+p2)/float(2)
    a3 = p1*(1-p1)
    a4 = p2*(1-p2)
    a5 = thr_lvl*(2*a2*(1-a2))**0.5
    a6 = thr_pow*(a3+a4)**0.5
    a7 = ((a5+a6)**2)/a1
    r = int(round(a7))
    return r


#数值情况
def func_sample_size_value(v1, v2, var1, var2, level, power):
    thr_lvl = thr_tscore_n_clvl(level)
    thr_pow = thr_tscore_n_power(power)
    r = int(round((var1 + var2) * ((thr_lvl + thr_pow)**2) / ((v1 - v2)**2)))
    return r

############# #############
