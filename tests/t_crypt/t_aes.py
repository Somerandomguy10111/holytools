from holytools.cryptography import AES
import os
#
# if __name__ == "__main__":
#     aes = AES()
#     encr = aes.encrypt( key='abc', content='a')
#     # encr = 'P3Ztyphjabpf9Kjm2JAFJJ2kMl1lmF4pR1w+qid6pPk7KI9gpQ=='
#     print(encr)
#
#     decr1 = aes.decrypt(key='abc', content=encr)
#     decr2 = aes.decrypt(key='aa', content=encr)
#
#     decr3 = AES().decrypt(key='abc', content=encr)
#     print(f'Correct key: {decr1}')
#     print(f'False key: {decr2}')
#     print(f'New instance, correct key: {decr2}')

if __name__ == "__main__":
    aes = AES()  # Initialize your AES encryption class
    aes_two = AES()

    # Test data
    test_content = "Hello, World!"
    test_key_str = "password123"
    test_key_bytes = os.urandom(32)  # Random 16-byte key
    test_content_empty = ""
    test_content_special = "特殊字符123"  # Include special and non-UTF-8 characters

    # Test cases
    print("1. Test Successful Encryption and Decryption with String Key:")
    encrypted = aes.encrypt(test_content, test_key_str)
    decrypted = aes.decrypt(test_key_str, encrypted)
    decrypted_two = aes_two.decrypt(test_key_str, encrypted)
    print(f"Encrypted: {encrypted}, Decrypted: \"{decrypted}\", Decrypted two \"{decrypted_two}\"")

    print("\n2. Test Successful Encryption and Decryption with Byte Key:")
    encrypted = aes.encrypt(test_content, test_key_bytes)
    decrypted = aes.decrypt(test_key_bytes, encrypted)
    print(f"Encrypted: {encrypted}, Decrypted: {decrypted}")

    print("\n3. Test Encryption and Decryption with Different Keys:")
    encrypted = aes.encrypt(test_content, test_key_str)
    decrypted = aes.decrypt("wrong_key", encrypted)
    print(f"Encrypted: {encrypted}, Decrypted: {decrypted or 'Decryption Failed'}")

    print("\n4. Test Handling of Empty String:")
    encrypted = aes.encrypt(test_content_empty, test_key_str)
    decrypted = aes.decrypt(test_key_str, encrypted)
    print(f"Encrypted: {encrypted}, Decrypted: '{decrypted}'")

    print("\n5. Test Handling of Special Characters and Non-UTF-8 Encoded Data:")
    encrypted = aes.encrypt(test_content_special, test_key_str)
    decrypted = aes.decrypt(test_key_str, encrypted)
    print(f"Encrypted: {encrypted}, Decrypted: {decrypted}")

    print("\n6. Test Decryption with Altered Encrypted Data:")
    encrypted = aes.encrypt(test_content, test_key_str)
    # Simulate data corruption by changing a byte
    if len(encrypted) > 1:  # Just a basic check to avoid index error
        altered_encrypted = encrypted[:-1] + chr((ord(encrypted[-1]) + 1) % 256)
    else:
        altered_encrypted = encrypted
    decrypted = aes.decrypt(test_key_str, altered_encrypted)
    print(f"Altered Encrypted: {altered_encrypted}, Decrypted: {decrypted or 'Decryption Failed'}")

    print("\n7. Test with Very Long String:")
    long_content = "A" * 10000  # Very long string of 'A's
    encrypted = aes.encrypt(long_content, test_key_str)
    decrypted = aes.decrypt(test_key_str, encrypted)
    print(f"Decrypted Length: {len(decrypted)}, Matches Original: {decrypted == long_content}")
