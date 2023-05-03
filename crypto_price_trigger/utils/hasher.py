from django.contrib.auth.hashers import PBKDF2PasswordHasher


class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    def encode(self, password, salt, iterations=None):
        """
        The encode function takes a password and salt, and returns the hashed
        password. It uses PBKDF2 with SHA256 as the hash algorithm; it also uses
        100000 iterations by default (overridable). The format of the string it
        returns is &quot;$id$iterations$salt$checksum&quot;, where id is &quot;pbkdf2_sha256&quot;.

        :param self: Represent the instance of the class
        :param password: Pass in the password that is being hashed
        :param salt: Add randomness to the password
        :param iterations: Determine the number of times to hash the password
        :return: A string of length 50
        """
        encoded = super().encode(password, salt, iterations)
        return encoded[:50]
