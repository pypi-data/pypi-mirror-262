import libnum
import gmpy2

def CommonMode(e1,e2,c1,c2,n):
    s,s1,s2 = gmpy2.gcdext(e1, e2)
    m = (pow(c1,s1,n) * pow(c2 ,s2 ,n)) % n
    return int(m)
