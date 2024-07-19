from holytools.cryptography import RSA


if __name__ == "__main__":
    rsa_crypto = RSA()
    private_key, public_key = RSA.get_key_pair()

    private_pem = RSA.get_pem(private_key, is_private=True)
    public_pem = RSA.get_pem(public_key, is_private=False)

    encrypted_message = rsa_crypto.encrypt('Hello, RSA!', public_pem)
    print('Encrypted:', encrypted_message)

    decrypted_message = rsa_crypto.decrypt(private_pem, encrypted_message)
    print('Decrypted:', decrypted_message)

