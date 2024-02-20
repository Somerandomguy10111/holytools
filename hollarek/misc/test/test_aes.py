from hollarek.crypt.encrypt import AES

if __name__ == "__main__":
    aes = AES()
    encr = aes.encrypt( key='abc', content='a')
    # encr = 'P3Ztyphjabpf9Kjm2JAFJJ2kMl1lmF4pR1w+qid6pPk7KI9gpQ=='
    print(encr)

    decr1 = aes.decrypt(key='abc', content=encr)
    decr2 = aes.decrypt(key='aa', content=encr)

    decr3 = AES().decrypt(key='abc', content=encr)
    print(f'Correct key: {decr1}')
    print(f'False key: {decr2}')
    print(f'New instance, correct key: {decr2}')


