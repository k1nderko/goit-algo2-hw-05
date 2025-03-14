import hashlib

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size  
        self.num_hashes = num_hashes  
        self.bit_array = [0] * size  

    def _hash(self, value, i):
        hash_value = hashlib.md5((value + str(i)).encode()).hexdigest()
        return int(hash_value, 16) % self.size

    def add(self, value):
        for i in range(self.num_hashes):
            index = self._hash(value, i)
            self.bit_array[index] = 1

    def check(self, value):
        for i in range(self.num_hashes):
            index = self._hash(value, i)
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(bloom_filter, passwords):
    results = {}
    for password in passwords:
        if password == "" or password is None:
            results[password] = "Некоректний пароль"
        elif bloom_filter.check(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")