import re

def get_mail_addresses_in_text(text: str) -> list[str]:
    username_part = r'[A-Za-z0-9._%+-]+'
    domain_part = r'[A-Za-z0-9.-]+'
    tld_part = r'[A-Z|a-z]{2,}'
    at_symbol = r'(?:@|\[at\]| \[at\] )'  # Non-capturing group

    email_pattern = fr'\b{username_part}{at_symbol}{domain_part}\.{tld_part}\b'

    mail_addresses = re.findall(email_pattern, text)
    mail_addresses = [address.replace(' [at] ', '@') for address in mail_addresses]
    mail_addresses = [address.replace('[at]', '@') for address in mail_addresses]

    return mail_addresses
