from hollarek.configs import LocalConfigs, AWSConfigs

if __name__ == "__main__":
    another_configs = LocalConfigs(config_fpath='abcd')
    local_confs = LocalConfigs()

    cloud_confs = AWSConfigs(secret_name='lotus_api_keys')
    cloud_confs.get(key='openai_api_key')


    print(local_confs.get(key='abcd'))
    print(cloud_confs.get(key='openai_api_keyy'))

