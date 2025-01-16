from holytools.configs import FileConfigs


def main():
    configs = FileConfigs(encrypted=True, fpath=f'~/.pyconfigs.txt')
    print(f'Credential store content')
    content = configs.read().strip()
    lines = content.split(f'\n')
    for l in lines:
        if len(l) > 0 and not l.startswith(f'['):
            l = f'├── {l}'
        print(l)



if __name__ == "__main__":
    main()