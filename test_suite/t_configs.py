from hollarek.io import LocalConfigs, AWSConfigs

if __name__ == "__main__":
    local_confs = LocalConfigs()
    another_configs = LocalConfigs(config_fpath='abcd')

    print(local_confs == another_configs)

    cloud_confs = AWSConfigs(secret_name='lotus_api_keys')
    cloud_confs.get(key='openai_api_key')


    print(local_confs.get(key='abcd'))
    print(cloud_confs.get(key='openai_api_keyy'))

