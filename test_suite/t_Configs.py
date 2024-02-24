from hollarek.io import LocalConfigs

if __name__ == "__main__":
    conf = LocalConfigs()
    print(conf.get(key='abcd'))