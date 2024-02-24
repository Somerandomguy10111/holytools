from hollarek.io import LocalConfigs, AWSConfigs

if __name__ == "__main__":
    another_configs = LocalConfigs(config_fpath='abcd')
    local_confs = LocalConfigs()

    print(local_confs == another_configs)
    print(local_confs.__class__ == another_configs.__class__)

    cloud_confs = AWSConfigs(secret_name='lotus_api_keys')
    cloud_confs.get(key='openai_api_key')


    print(local_confs.get(key='abcd'))
    print(cloud_confs.get(key='openai_api_keyy'))

