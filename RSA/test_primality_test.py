from rsa import mr_primality_test
import os


P300_2=987803022049986277135970067344834622462454497299773392125226379865108836890801465494624453732220262575620990176677624787173368810199864691227980099140734912747109176534020886580539516654681674464870587081374854510850595347202744051176551109119165716536047263217664666996662170882630042947238466043371


if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'Testing/Data/export_6.txt')
    test=open(filename,"r")
    
    lines=test.readlines()
    for line in lines:
        line=line.split('\t')
        for prime in line:
            prime=prime.strip('\n')
            print(prime,": ",mr_primality_test(2, int(prime)))
    
    
    
    print(f"{mr_primality_test(3, P300_2)=}")