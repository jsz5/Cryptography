import random
from random import randint

from Cryptodome.Cipher import AES

s = 20
N = 2 ** 16
n = 256


def generate_all_binary(length, binary, binaries, i):
    if i == length:
        binaries.append(''.join(map(str, binary)))
        return
    binary[i] = 0
    generate_all_binary(length, binary, binaries, i + 1)

    binary[i] = 1
    generate_all_binary(length, binary, binaries, i + 1)


def random_binary(length):
    binary = ""
    for i in range(length):
        binary += str(random.randint(0, 1))
    return binary


def binary_to_bytes(binary):
    return int(binary, 2).to_bytes((len(binary) + 7) // 8, byteorder='big')


def encryption():
    keys = []
    msgs = []
    for i in range(0, N):
        secret_binary = random_binary(s)
        key_string = "1" * (n - s) + secret_binary
        key = binary_to_bytes(key_string)
        keys.append(key_string)
        enc_suite = AES.new(key, AES.MODE_GCM, key)
        msg = enc_suite.encrypt(bytes(key_string + "SECRET MESSAGE", encoding='utf-8'))
        msgs.append(msg)
    return keys, msgs


def decryption(keys, msgs):
    decrypted_msg = ''
    random_identifier = randint(0, N - 1)
    all_binaries = []
    generate_all_binary(s, [None] * s, all_binaries, 0)
    all_binaries_length=2**s
    for i, secret_binary in enumerate(all_binaries):
        print(f"Check number {i}/{all_binaries_length}")
        key_string = "1" * (n - s) + secret_binary
        key = binary_to_bytes(key_string)
        dec_suite = AES.new(key, AES.MODE_GCM, key)
        decrypted_msg = dec_suite.decrypt(msgs[random_identifier])
        if decrypted_msg.startswith(bytes("1" * (n - s), encoding='utf-8')):
            print("SUCCESS")
            break

    print("Decrypted cryptogram:")
    print(f"identifier: {random_identifier}")
    print(f"secret_key: {key_string}")
    print(f"message: {decrypted_msg[n:]}")
    print("----------------")
    print(f"Encrypted key: {keys[random_identifier]}")


if __name__ == '__main__':
    keys, msgs = encryption()
    print("Encrypted. Brute force decryption")
    decryption(keys, msgs)
