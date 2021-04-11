import binascii
import hashlib
import subprocess
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def hash_message(message):
    hashed_message=hashlib.md5(message.read().encode('utf-8')).hexdigest()
    magic_bytes='3020300c06082a864886f70d020505000410'
    k=360
    number_of_f=int(((k/8)-(len(hashed_message)/2+len(magic_bytes)/2+3))*2)
    padding_f="f"*number_of_f
    padding=f'0001{padding_f}00'
    return int(f'{padding}{magic_bytes}{hashed_message}', 16)


padded_hash = hash_message(open("./files/grade.txt","r"))
modulus =subprocess.check_output("./modulus.sh", stderr=subprocess.STDOUT, shell = True)
n = int(modulus,16)
e=65537
phi=((1524938362073628791222322453937223798227099080053904149-1)*(1385409854850246784644682622624349784560468558795524903-1))
gcd, x, y = egcd(e, phi)
d = modinv(e, phi)
sign = hex(pow(padded_hash, d, n))[2:]
with open("./files/grade_forge.sign","wb") as f:
    f.write(binascii.unhexlify(sign))
