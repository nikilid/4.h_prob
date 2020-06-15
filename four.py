import random
import math
import base64
import sys
import json
import numpy 

mes = []
al = []
l_col = []

def gen( n,  d, i):
    for j in range(2):
        d[i] = j
        if (i == n-1):
            mes.append(list(d))
        else:
            gen( n, d, i+1)

def gen1( n,  d, i):
    for j in range(2):
        d[i] = j
        if (i == n-1):
            al.append(list(d))
        else:
            gen1( n, d, i+1)

def check_g(d, t):
    count = 0
    for i in range(len(d)):
        count += d[i]
    if (count == t):
        l_col.append(d)

def gen2(n,d, i, t):
    for j in range(2):
        d[i] = j
        if (i == n-1):
            check_g(list(d), t)
        else:
            gen2( n, d, i+1, t)

def check(H, r, n, t):
    t = t - 1
    H_t = numpy.array(H).transpose()
    d = r*[0]
    gen2(r, d, 0, t)
    su = numpy.array(n*[0])
    for num in l_col:
        for i in range(r):
            if (num[i] == 1):
                su += H[i]
                flag = 1
                for j in range(n):
                    if (su[j] == 1):
                        flag = 0
                if (flag):
                    return True
        su = numpy.array(n*[0])
    return False





def do_code(fil, r, n, p):
    t = int(n*p)
    k = n - r
    d = [0]*k
    gen(k, d, 0)
    G = []
    H = []
    for i in range(r):
        l = n*[0]
        H.append(list(l))   
    for i in range(k, n, 1):
        H[i-k][i] = 1
    flag = 1
    while flag:
        for j in range(r):
            for i in range(k):
                H[j][i] = random.randint(0,1)
        flag = check(H, r, n, t)
    for i in range(k):
        l = n*[0]
        G.append(list(l)) 
    for i in range(k):
        G[i][i] = 1
        for j in range(k, n, 1):
            G[i][j] = H[j-k][i]

    code = {}
    G_mat = numpy.array(G)
    H_mat = numpy.array(H)
    for m in mes:
        l = list(m)
        a = numpy.array(l)
        res = a.dot(G_mat)
        for i in range(n):
            res[i] %= 2 
        code[str(m)] = res

    
    q = (1 << r) - 1
    d = [0]*n
    gen1(n, d, 0)
    ans = {}
    v = 0 
    for i in range(q):
        b = numpy.array(al[v])
        v+=1
        flag = 1
        while (flag):
            for ch in sorted(code):
                if (str(b) == str(code[ch])):
                    b = numpy.array(al[v])
                    v+=1
                    flag = 1
                    break
                else:
                    flag = 0
               
        l = []
        l1 = []
        f = 1
        for ch in sorted(code):
            res = numpy.array(n*[0])
            count = 0
            count1 = 0
            for j in range(n):
                res[j] = b[j]^code[ch][j]
                count+=res[j]
                count1 += code[ch][j]
            st = ''.join(str(e) for e in res.tolist())
            l.append((count, st ) )
            st = ''.join(str(e) for e in code[ch].tolist())
            l1.append((count1, st ) )
            if (f == 1):
                s1 = H_mat.dot(code[ch].transpose())
                f = 0
            s = H_mat.dot(res.transpose())
        l_res = []
        l_res1 = []
        for it in sorted(l):
            l_res.append(it[1])
        for it in sorted(l1):
            l_res1.append(it[1])
        ans[''.join(str(e%2) for e in s.tolist())] = (l_res)
        ans[''.join(str(e%2) for e in s1.tolist())] = (l_res1)
    fil.write(str(k)+'\n')
    fil.write(str(n)+'\n')
    fil.write('{')
    for ch in sorted(code):
        #print("{} : {}".format(''.join(str(e) for e in eval(ch)), ''.join(str(e) for e in code[ch].tolist())))
        fil.write("{} : {}, ".format('"' +''.join(str(e) for e in eval(ch))+'"', '"'+ ''.join(str(e) for e in code[ch].tolist()) +'"'))
    fil.write('}\n')
    fil.write(str(H))
    fil.write('\n')
    fil.write('{')
    for ch in sorted(ans):
        #print("{} : {}".format((ch), ans[ch]))
        fil.write("{} : {}, ".format('"' +str(ch) +'"', '"' + str(ans[ch]) + '"'))
    fil.write('}\n')

def enc(f_code, text, e):
    fi = open(f_code, 'r')
    code = ''
    vv = ''
    k = int(fi.readline())
    n = int(fi.readline())
    code += (fi.readline())
    H = (fi.readline())
    vv += (fi.readline())
    code = eval(code)
    res = ''
    while(text != ''):    
        for i in code:
            if text.startswith(i):
                res += code[i]
                text = text[len(i):]
    if (e == "None"):
        e = ''
        for i in range(len(res)):
            e += str(random.randint(0,1))
    a = numpy.array(list(res))
    e_mat = numpy.array(list(str(e)))
    err = numpy.array(len(res)*[0])
    for i in range(len(res)):
        err[i] = int(a[i]) ^ int(e_mat[i])
    print('Результат кодирования: ', res)
    err = ''.join(str(e) for e in (err))
    print('Результат наложения ошибки: ',err)
    print('Вектор ошибки: ', e)


def dec(f_code, text):
    fi = open(f_code, 'r')
    code = ''
    vv = ''
    k = int(fi.readline())
    n = int(fi.readline())
    code += (fi.readline())
    H = (fi.readline())
    vv += (fi.readline())
    code = eval(code)
    decode = {}
    for i in code:
        decode[code[i]] = i
    vv = eval(vv)
    H_mat = numpy.array(eval(H))
    res = ''
    s_er = ''
    while(text != ''): 
        val = text[:n]  
        val1 = numpy.array(list(n*[0]))
        for j in range(n):
            val1[j] = int(val[j])
        s = H_mat.dot(val1.transpose())
        w = vv[''.join(str(e%2) for e in s.tolist())]
        w = eval(w)
        s_er += w[0]
        err = numpy.array(list(w[0]))
        v = numpy.array(n*[0])
        for i in range(n):
            v[i] = int(err[i]) ^ int(val1[i])
        c =  ''.join(str(e) for e in v.tolist())
        res += decode[c]
        text = text[n:]
    print("Вектор ошибки: ", s_er)
    print("Декодированное сообщение: ", res)


    
if (int(sys.argv[1]) == 1):
    f = open("result1.txt", 'w')
    r = eval(sys.argv[2])
    n = eval(sys.argv[3])
    p = eval(sys.argv[4])
    do_code(f, r,n,p)
else:
    if (int(sys.argv[1]) == 2):
        e = "None"
        f_code = sys.argv[2]
        m = (sys.argv[3])
        if (len(sys.argv) == 5):
            e = (sys.argv[4])
        enc(f_code, m, e)
    else:
        if (int(sys.argv[1]) == 3):
            f_code = sys.argv[2]
            m = (sys.argv[3])
            dec(f_code, m)

