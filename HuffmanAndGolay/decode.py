import heapq
import sys

G1=[[1,0,0,1,0],[0,1,0,1,1],[0,0,1,1,0]]
U1=[[1,0,0,0,1]]

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
                    new_priority = sum(index * index for index in new_indexes)
                    heapq.heappush(queue, (new_priority, new_indexes))
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
    p=generalobol_ellenorzo_matrix(generalo_matrix)
    print_matrix(p)
    
    print("Szindróma:")
    szindroma=matrix_szorzas(kodszo,p)
    print_matrix(szindroma)
    
    print("Szindróma keresés:")
    hiba_vektor=[]
    legkisebb_hiba=len(kodszo[0])
    for i in generate_error_vector(range(base), len(kodszo[0])):
        i=[list(i)]
        if matrix_szorzas(i,p) == szindroma:
            if count_error_bits(i[0])>legkisebb_hiba:
                break
            elif count_error_bits(i[0]) == legkisebb_hiba:
                print("Több mint 1 db legközelebbi kódszó!")
                sys.exit()
            else:
                legkisebb_hiba = count_error_bits(i[0])
                hiba_vektor=i
                
    print("Hiba vektor:")
    print_matrix(hiba_vektor)      
    print("Javított kód:")
    javitott=vektor_kivonas(kodszo[0], hiba_vektor[0], base)
    print_matrix([javitott])
    print("Ellenőrzés:")
    ellenorzo_szorzat = matrix_szorzas([javitott], p, base)
    print_matrix(ellenorzo_szorzat)

# ((szám % modulus) + modulus) % modulus
if __name__ == "__main__":
    decode(GOLAY_G1, GOLAY_U1_2_ERROR, 2)
    # decode(G1, U1, 2)
    
    # for tup in generate_error_vector(range(0, 2), 3):
    #    print(tup)

        
    