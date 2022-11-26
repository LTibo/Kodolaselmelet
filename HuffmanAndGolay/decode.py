import heapq
import sys

G1_2=[[1,0,0,1,0],[0,1,0,1,1],[0,0,1,1,0]]
G2_3=[[1,0,1,2],[0,1,1,1]]
U1_1_ERROR_BASE_2=[[1,0,0,0,1]]
U2_0_ERROR_BASE_3=[[2,1,0,2]]
U3_1_ERROR_BASE_3=[[1,2,1,0]]


GOLAY_G1=[[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0,],
          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1,],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1,],
          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0,],
          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1,],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1,],
          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1,],
          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1,]]

GOLAY_U1_2_ERROR=[[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,]]
GOLAY_U2_3_ERROR=[[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,]]
GOLAY_U3_4_ERROR_FAIL=[[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,]]

def print_matrix(m:list):
    for sor in m:
        for elem in sor:
            print(elem, end=" ")
        print("")


def generalobol_ellenorzo_matrix(g:list,base:int=2):
    ellenorzo=[]
    for sor in g:
        ellenorzo.append(sor[len(g):])
    
    # -1-el szorzas
    for sor_i, sor in enumerate(ellenorzo):
        for elem_i, elem in enumerate(sor):
            ellenorzo[sor_i][elem_i]=((((((elem*-1)% base) + base)%base)% base) + base)%base

    # print(ellenorzo)

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

#először 1 hibásakat, utána 2, utána 3 stb, generál
def generate_error_vector(sequence, repeat):
    repeated_sequence=[]
    for i in range(repeat):
        repeated_sequence.append(sequence)
    start = (0,)*len(repeated_sequence)
    queue = [(0, start)]
    seen = set([start])
    while queue:
        _, indexes = heapq.heappop(queue)
        yield tuple(seq[index] for seq, index in zip(repeated_sequence, indexes))
        for i in range(len(repeated_sequence)):
            if indexes[i] < len(repeated_sequence[i]) - 1:
                lst = list(indexes)
                lst[i] += 1
                new_indexes = tuple(lst)
                if new_indexes not in seen:
                    new_priority = count_error_bits(new_indexes)
                    heapq.heappush(queue, (new_priority, new_indexes))
                    # print(f"{new_indexes=}")
                    # print(f"{new_priority=}")
                    # print(f"{queue=}")
                    seen.add(new_indexes)


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

def decode(generalo_matrix:list, kodszo:list, base:list):
    print("Kódolt üzenet:")
    print_matrix(kodszo)
    print("Ellenőrző mátrix:")
    p=generalobol_ellenorzo_matrix(generalo_matrix, base)
    print_matrix(p)
    
    print("Szindróma:")
    szindroma=matrix_szorzas(kodszo,p, base)
    print_matrix(szindroma)
    
    print("Szindróma keresés:")
    hiba_vektor=[]
    legkisebb_hiba=len(kodszo[0])
    for i in generate_error_vector(range(base), len(kodszo[0])):
        i=[list(i)]
        if matrix_szorzas(i,p, base) == szindroma:
            if count_error_bits(i[0])>legkisebb_hiba:
                break
            elif count_error_bits(i[0]) == legkisebb_hiba:
                print(f"Több mint 1 db legközelebbi kódszó! (legalább {legkisebb_hiba} helyen hiba)")
                sys.exit()
            else:
                legkisebb_hiba = count_error_bits(i[0])
                hiba_vektor=i
                
    print(f"Hiba vektor ({legkisebb_hiba} helyen hibás):")
    print_matrix(hiba_vektor)      
    print("Javított kód:")
    javitott=vektor_kivonas(kodszo[0], hiba_vektor[0], base)
    print_matrix([javitott])
    print("Ellenőrzés:")
    ellenorzo_szorzat = matrix_szorzas([javitott], p, base)
    print_matrix(ellenorzo_szorzat)

# ((szám % modulus) + modulus) % modulus
if __name__ == "__main__":
    decode(G1_2, U1_1_ERROR_BASE_2, 2)
    print("--------------------")
    decode(G2_3,U2_0_ERROR_BASE_3, 3)
    print("--------------------")
    decode(G2_3,U3_1_ERROR_BASE_3, 3)
    print("--------------------")
    decode(GOLAY_G1, GOLAY_U1_2_ERROR, 2)
    print("--------------------")
    decode(GOLAY_G1, GOLAY_U2_3_ERROR, 2)
    print("--------------------")
    decode(GOLAY_G1, GOLAY_U3_4_ERROR_FAIL, 2)
    
    
    # for tup in generate_error_vector(range(0, 3), 3):
    #     print(tup)

        
    