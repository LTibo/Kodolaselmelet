import time
import os

#CONSTANTS

A=2
P3_1=561
P4_1=2129
P4_2=7919
P50_1=13028317441145613048590061985388937770807889867209
P300_1=418935665971635472851313446571463339584979301560842377758748758164833583501175687936063039370886243305685565007772947619136941212910832585955786954057597686446358493529046645312686416471967277388347161795818502950943879042333390829966913426040692197740642654317185348516362135306322034813076900210333
P300_2=987803022049986277135970067344834622462454497299773392125226379865108836890801465494624453732220262575620990176677624787173368810199864691227980099140734912747109176534020886580539516654681674464870587081374854510850595347202744051176551109119165716536047263217664666996662170882630042947238466043371

#FUNCTIONS

#gyors hatvanyozas 
def fast_modular_exponentiation(a:int, n:int, r:int, m:int) -> int:
    i=1
    res=a
    a_list:list=[i]
    mod_res_list:list=[res]
    while ((i*2)<=m):
        i*=2
        res=(res*res)%n
        a_list.append(i)
        mod_res_list.append(res)

    diff=m-i

    supplementary_element_indexes:list=[]
    for ind, e in reversed(list(enumerate(a_list))):
        if e <= diff and diff-e>=0:
            diff-=e
            supplementary_element_indexes.append(ind)

    #calculating a^m
    a_on_m=res
    for ind in supplementary_element_indexes:
        a_on_m=(a_on_m*mod_res_list[ind])%n

    res=a_on_m

    #calculating the rest
    q=1
    while (q<=r):
        q+=1
        res=(res*res)%n

    return res              

#gyors hatvanyozas
def mr_primality_test(a:int, n:int):
    if n==2:
        return True

    if (n<3 or n%2==0):
        return False

    r,m = calc_r_and_m(n)

    i=1
    res=a
    a_list:list=[i]
    mod_res_list:list=[res]
    while (True):
        i*=2
        res=(res*res)%n
        a_list.append(i)
        mod_res_list.append(res)

        if (i*2)>m:
            break

    diff=m-i

    supplementary_element_indexes:list=[]
    for ind, e in reversed(list(enumerate(a_list))):
        if e <= diff and diff-e>=0:
            diff-=e
            supplementary_element_indexes.append(ind)   

    #calculating a^m
    a_on_m=res
    for ind in supplementary_element_indexes:
        a_on_m=(a_on_m*mod_res_list[ind])%n

    res=a_on_m
    a_list.append(m)
    mod_res_list.append(res)
    
    #computing the rest
    i=1
    q=1
    mod_res_list_part_2=[res]
    while (q<=r):            
        i*=2
        q+=1
        res=(res*res)%n

        mod_res_list_part_2.append(res)

        a_list.append(i)
        mod_res_list.append(res)

        

    #print(a_list)
    #print(mod_res_list)

    #check
    for element in reversed(mod_res_list_part_2):
        if element==1:
            continue
        elif element==n-1:
            return True
        else:
            return False     

    return True

def calc_r_and_m(n:int):
    n_minus_one=n-1
    r=0
    m=1
    rem=0
    res=n_minus_one
    two_on_r=1
    while(True):
        rem=res%2
        if (rem==0):
            res=res//2
            r=r+1
            two_on_r*=2
        else:          
            break
    m=n_minus_one//two_on_r
    # print("r:",r,"m:",m)     
    return r,m      

def greatest_common_divisor(k:int, l:int):
    if k == l: 
        return 0
    elif k == 0 or l == 0:
        return k
    else:
        if k > l:
            return greatest_common_divisor(k-l, l)
        else:
            return greatest_common_divisor(k, l-k)        


def key_generation(p:int, q:int) -> tuple[int, int]:
    #two prime numbers: p, q

    #product
    product=p*q

    #calculate totient
    totient=(p-1)*(q-1)

    #select public key
    public_key=2
    while(public_key<totient):
        if mr_primality_test(A, public_key) and greatest_common_divisor(totient, public_key)==1:
            break
        elif public_key==2:
            public_key+=1
        else:
            public_key+=2
    #print(public_key)            

    #select private key: (private_key*public_key) mod totient = 1



if __name__ == "__main__":

    start_time = time.time()
    key_generation(7, 19)
    print("--- %s seconds ---" % (time.time() - start_time))


    # dir = os.path.dirname(__file__)
    # filename = os.path.join(dir, 'Testing/Data/export_6.txt')
    # test=open(filename,"r")
    
    # lines=test.readlines()
    # for line in lines:
    #     line=line.split('\t')
    #     for prime in line:
    #         prime=prime.strip('\n')
    #         print(prime,": ",mr_primality_test(A, int(prime)))

