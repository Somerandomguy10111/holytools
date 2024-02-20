from hollarek.misc.crypt import AES

if __name__ == "__main__":
    aes = AES()
    encr = aes.encrypt(content='abcd', key='abcd')

    decr1 = aes.decrypt(key='abcd', content=encr)
    decr2 = aes.decrypt(key='aa', content=encr)
    print(decr1)