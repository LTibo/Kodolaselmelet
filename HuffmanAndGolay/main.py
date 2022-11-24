


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

def matrix_szorzas(m1:list, m2:list):
    if len(m1[0]) != len(m2):
        return None
    
    szorzat=[]
    for i, m1_sor in enumerate(m1):
        uj_sor=[]
        for j, m2_oszlop in enumerate(m2[i]):
            uj_sor.append(m1_sor[j]*m2_oszlop)

        szorzat.append(uj_sor)
    
    return szorzat   
            


if __name__ == "__main__":
    p=generalobol_ellenorzo_matrix(G1)
    # print(p)
    # print_matrix(p)
    print_matrix(matrix_szorzas(U1,p))