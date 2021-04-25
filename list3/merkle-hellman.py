import random

from gmpy2 import invert


class MerkleHellman:

    def __init__(self):
        self.n = 50 * 8  # number of max bits to encode
        self.b = []
        self.w = []
        self.q = 0
        self.r = 0
        self.generate_keys()

    def generate_keys(self):
        max_number = 2 ** 40
        self.w.append(random.randint(1, max_number))
        sequence_sum = self.w[0]
        for i in range(1, self.n):
            self.w.append(sequence_sum + random.randint(1, max_number))
            sequence_sum += self.w[i]

        self.q = sequence_sum + random.randint(1, max_number)
        self.r = self.q - 1
        for i in range(self.n):
            self.b.append((self.w[i] * self.r) % self.q)

    def encrypt(self, message):
        binary = ''.join('{:08b}'.format(i) for i in bytes(message, encoding='utf8')).zfill(self.n)
        c = 0
        for i in range(len(binary)):
            c += self.b[i] * int(binary[i], 2)
        return c

    def decrypt(self, cypher):
        decrypted_binary = ""
        c = (int(cypher) * invert(self.r, self.q)) % self.q
        for i in range(len(self.w) - 1, -1, -1):
            if self.w[i] <= c:
                c -= self.w[i]
                decrypted_binary += "1"
            else:
                decrypted_binary += "0"
        decrypted_binary = decrypted_binary.rstrip("0")[::-1]
        return int(decrypted_binary, 2).to_bytes((len(decrypted_binary) + 7) // 8, 'big').decode()


if __name__ == "__main__":
    crypto = MerkleHellman()
    message = "SECRET MESSAGE"
    print(f"Message to encrypt: {message}")
    encrypted = crypto.encrypt(message)
    print(f"Encrypted message: {encrypted}")
    decrypted = crypto.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
