import time
import os
from dataclasses import dataclass
import random

#CONSTANTS

A=2
P3_1=561
P4_1=2129
P4_2=7919
P10_1=2266158563
P10_2=6794445407
P15_1=234620322075379
P15_2=897229386310259
P50_1=13028317441145613048590061985388937770807889867209
P100_1=7608367794680566508765526190236443829666887048709765014048513900924574414466301018547920587791917867
P100_2=7022907309745430185208014885989351945610218402731987260517312382397948158487451741511130965746576191
P300_1=418935665971635472851313446571463339584979301560842377758748758164833583501175687936063039370886243305685565007772947619136941212910832585955786954057597686446358493529046645312686416471967277388347161795818502950943879042333390829966913426040692197740642654317185348516362135306322034813076900210333
P300_2=987803022049986277135970067344834622462454497299773392125226379865108836890801465494624453732220262575620990176677624787173368810199864691227980099140734912747109176534020886580539516654681674464870587081374854510850595347202744051176551109119165716536047263217664666996662170882630042947238466043371

#STRUCTS

@dataclass
class Extended_euclidian_line:
    quotient: int
    remainder: int
    s: int
    t: int

#FUNCTIONS

#gyors hatvanyozas 
def fast_modular_exponentiation(a:int, m:int, n:int) -> int:
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

    return a_on_m              

#prim teszt
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

def greatest_common_divisor(a:int, b:int):
    if b == 0:
        return a
    else:
        return greatest_common_divisor(b, a%b)          


def extended_euclidian(a:int, b:int) -> tuple[int, int, int]:
    
    l=0 #larger value
    s=0 #smaller value
    if a > b:
        l=a
        s=b
    else:
        l=b
        s=a

    i0=Extended_euclidian_line(None, l, 1, 0)

    i1=Extended_euclidian_line(None, s, 0, 1)

    gcd=None
    Bezout_coefficient_1=None
    Bezout_coefficient_2=None
    table=[i0,i1]
    i=2
    while(True):
        
        quotient=table[i-2].remainder//table[i-1].remainder
        remainder=table[i-2].remainder-(quotient*table[i-1].remainder)
        s=table[i-2].s-(quotient*table[i-1].s)
        t=table[i-2].t-(quotient*table[i-1].t)

        line=Extended_euclidian_line(quotient, remainder, s, t)

        

        if line.remainder==0:
            gcd=table[i-1].remainder
            Bezout_coefficient_1=table[i-1].s 
            Bezout_coefficient_2=table[i-1].t
            break

        i+=1
        table.append(line)

    #print(Bezout_coefficient_1, Bezout_coefficient_2, gcd)
    return Bezout_coefficient_1, Bezout_coefficient_2, gcd   


def key_generation(p:int, q:int) -> tuple[int, int, int]:
    #two prime numbers: p, q

    #product
    product=p*q

    #calculate totient
    totient=(p-1)*(q-1)

    #select public key
    public_key=random.randrange(3, 3+(totient//10), 2)
    while(public_key<totient):
        _, _, gcd = extended_euclidian(public_key, totient)
        if mr_primality_test(A, public_key) and gcd==1:
            break
        elif public_key==2:
            public_key+=1
        else:
            public_key+=2           

    #select private key: (private_key*public_key) ≡ 1 mod(totient)
    private_key=None
    Bezout_coefficient_1, Bezout_coefficient_2, gcd = extended_euclidian(public_key, totient)

    if (Bezout_coefficient_1*public_key)%totient==1:
        private_key=Bezout_coefficient_1
    else:
        private_key=Bezout_coefficient_2    

    while (private_key<0):
        private_key+=totient

    return private_key, public_key, product

def encrypt(public_key:int, message:int, modulus:int) ->int:
    return fast_modular_exponentiation(message, public_key, modulus)

def decrypt(private_key:int, message:int, modulus:int) -> int:
    return fast_modular_exponentiation(message, private_key, modulus)

if __name__ == "__main__":
    mode=input("Select a mode (press \"g\" for key pair generation, \"e\" for message encryption, \"d\" for decryption): ")

    if mode=="g":
        p=input("Value of p: ")
        q=input("Value of q: ")
        if not mr_primality_test(A, int(p)):
            print(f"{p} is composite")
            exit()
        if not mr_primality_test(A, int(q)):
            print(f"{q} is composite")
            exit()

        start_time = time.time()
        private_key, public_key, n = key_generation(int(p),int(q))
        print("--------")
        print("Key generation: %s seconds" % (time.time() - start_time))
        print("--------")

        print(f"Public key:\n{public_key}")
        print("----------------------------------------")
        print(f"Modulus:\n{n}")
        print("----------------------------------------")
        print(f"Private key:\n{private_key}")
        print("----------------------------------------")
    elif mode=="e":
        e=input("Encryption key: ")
        print("----------------------------------------")
        m=input("Modulus: ")
        print("----------------------------------------")
        message=input("Message(integer): ")
        print("----------------------------------------")

        print(f"Encrypted message:\n{encrypt(int(e), int(message), int(m))}")
        print("----------------------------------------")
    elif mode=="d":
        e=input("Decryption key: ")
        print("----------------------------------------")
        m=input("Modulus: ")
        print("----------------------------------------")
        message=input("Message(integer): ")
        print("----------------------------------------")

        print(f"Decrypted message:\n{decrypt(int(e), int(message), int(m))}")
        print("----------------------------------------")
    else:
        print("Unrecognised command!")


    # dir = os.path.dirname(__file__)
    # filename = os.path.join(dir, 'Testing/Data/export_6.txt')
    # test=open(filename,"r")
    
    # lines=test.readlines()
    # for line in lines:
    #     line=line.split('\t')
    #     for prime in line:
    #         prime=prime.strip('\n')
    #         print(prime,": ",mr_primality_test(A, int(prime)))

