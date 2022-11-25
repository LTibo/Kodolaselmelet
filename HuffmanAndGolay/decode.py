from itertools import product
import sys

A=[[1,0,1], [2,1,1], [0,1,1], [1,1,2]]
B=[[1,2,1], [2,3,1], [4,2,2]]


G1=[[1,0,0,1,0],[0,1,0,1,1],[0,0,1,1,0]]
U1=[[1,0,0,0,1]]
T=2

def print_matrix(m:list):
    for sor in m:
        for elem in sor:
            print(elem, end=" ")
        print("")


def generalobol_ellenorzo_matrix(g:list):
    ellenorzo=[]
    for sor in g:
        ellenorzo.append(sor[len(g):])
    
    one_index=0
    ellenorzo_sor_len=len(ellenorzo[0])
    for sor in range(ellenorzo_sor_len):
        ellenorzo.append([])
        for elem_index in range(ellenorzo_sor_len):
            if elem_index==one_index:
                ellenorzo[-1].append(1)
            else:
                ellenorzo[-1].append(0)
        one_index+=1
    
    return ellenorzo

def matrix_szorzas(m1:list, m2:list, base:int=2):
    if len(m1[0]) != len(m2):
        return None
    
    szorzat=[[((sum(a*b for a,b in zip(A_sor, B_oszlop))% base) + base)%base for B_oszlop in zip(*m2)] for A_sor in m1]
    
    return szorzat   
            

def generate_error_vector(vector_length:int, base:int=2):
    return product(range(0,base), repeat=vector_length)


def count_error_bits(vector:list):
    error_count=0
    for i in vector:
        if i != 0:
            error_count+=1
    return error_count

def vektor_kivonas(v1:list, v2:list, base:int=2):
    if len(v1) != len(v2):
        return None

    kulonbseg_vektor=[]
    for i1, i2 in zip(v1, v2):
        kulonbseg_vektor.append((((i1-i2) % base) + base)%base)
    return kulonbseg_vektor

# ((szám % modulus) + modulus) % modulus
if __name__ == "__main__":
    base=2
    print("Kódolt üzenet:")
    print_matrix(U1)
    print("Ellenőrző mátrix:")
    p=generalobol_ellenorzo_matrix(G1)
    print_matrix(p)
    
    print("Szindróma:")
    szindroma=matrix_szorzas(U1,p)
    print_matrix(szindroma)
    
    print("Szindróma keresés:")
    hiba_vektorok=[]
    legkesvesebb_hiba=0
    for i in generate_error_vector(len(U1[0]), base):
        i=[list(i)]
        if matrix_szorzas(i,p) == szindroma:
            hiba_vektorok.append((count_error_bits(i[0]),i))
    
    hiba_vektorok=sorted(hiba_vektorok, key=lambda x:x[0])
    # print(hiba_vektorok)
    
    if hiba_vektorok[0][0] == hiba_vektorok[1][0]:
        print("Több mint 1 db legközelebbi kódszó!")
    else:
        print("Javított kód:")
        javitott=vektor_kivonas(U1[0], hiba_vektorok[0][1][0], base)
        print(javitott)
        print("Ellenőrzés:")
        ellenorzo_szorzat = matrix_szorzas([javitott], p, base)
        print_matrix(ellenorzo_szorzat)
        
    