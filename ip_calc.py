"""
GitHub link: https://github.com/alorthius/lab1_ip_calc
"""


def check_users_input(raw_address: str) -> str:
    """
    Check user's input. If it is not a string, return None.
    If it does not contain mask prefix, return 'Missing prefix'.
    If ip is not correct, return 'Error'.
    If all rules are satisfied, return True.

    >>> check_users_input(155)

    >>> check_users_input(['230', '248', '10', '10'])

    >>> check_users_input('230.248.10.10')
    'Missing prefix'
    >>> check_users_input('366.248.10.10/20')
    'Error'
    >>> check_users_input('230.248.10.10/77')
    'Error'
    >>> check_users_input('366.248/20')
    'Error'
    >>> check_users_input('230.248.10.10/20')
    True
    """
    if not isinstance(raw_address, str):
        return None

    elif '/' not in raw_address:
        return 'Missing prefix'

    mask = int(raw_address[raw_address.find('/') + 1:])
    if mask < 0 or mask > 32:
        return 'Error'

    new_address = raw_address[:raw_address.find('/')].split('.')
    if len(new_address) != 4:
        return 'Error'

    for number in new_address:
        if int(number) < 0 or int(number) > 255:
            return 'Error'

    return True


def get_ip_from_raw_address(raw_address: str) -> str:
    """
    Return ip-address.
    Return None, if the argument is not a string.

    >>> get_ip_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    >>> get_ip_from_raw_address(['91', '123', '130', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    return raw_address[: raw_address.find('/')]


def get_binary_ip(ip_address: str) -> str:
    """
    Return binary ip address.
    Return None, if the argument is not a string.

    >>> get_binary_ip('91.124.230.205')
    '01011011.01111100.11100110.11001101'
    >>> get_binary_ip(['91', '124', '230', '205'])

    """
    if not isinstance(ip_address, str):
        return None

    ip_list = ip_address.split('.')
    binary_ip = []

    for num in ip_list:
        binary_num = str(bin(int(num)))[2:]

        if len(binary_num) != 8:
            binary_num = '0' * (8 - len(binary_num)) + binary_num
        binary_ip.append(binary_num)

    return '.'.join(binary_ip)


def get_mask_number(raw_address: str) -> int:
    """
    Return mask nu,ber as an integer.
    Return None, if the argument is not a string.

    >>> get_mask_number('91.124.230.205/30')
    30
    >>> get_mask_number(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    return int(raw_address[raw_address.find('/') + 1:])


def get_binary_mask_from_raw_address(raw_address: str) -> str:
    """
    Return binart mask.
    Return None, if the argument is not a string.

    >>> get_binary_mask_from_raw_address('91.124.230.205/30')
    '11111111.11111111.11111111.11111100'
    >>> get_binary_mask_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    empty_mask = '00000000.00000000.00000000.00000000'
    mask_num = get_mask_number(raw_address)
    binary_mask = empty_mask.replace('0', '1', mask_num)
    return binary_mask


def convert_binary_to_numbers(binary_row: str) -> str:
    """
    Convert ip or network addresses or mask from binary
    to the regular one and return in as a string.
    Return None, if the argument is not a string.

    >>> convert_binary_to_numbers('01011011.01111100.11100110.11001101')
    '91.124.230.205'
    >>> convert_binary_to_numbers(['01011011', '01111100', '11100110', '11001101'])

    """
    if not isinstance(binary_row, str):
        return None

    return '.'.join([str(int(num, 2)) for num in binary_row.split('.')])


def get_network_address_from_raw_address(raw_address: str) -> str:
    """
    Get and return network address.
    Return None, if the argument is not a string.

    >>> get_network_address_from_raw_address('91.124.230.205/30')
    '91.124.230.204'
    >>> get_network_address_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    binary_ip = get_binary_ip(get_ip_from_raw_address(raw_address))
    binary_mask = get_binary_mask_from_raw_address(raw_address)

    network_address = []
    for ip_index, ip_num in enumerate(binary_ip):
        for mask_index, mask_num in enumerate(binary_mask):
            if ip_index == mask_index:
                try:
                    network_address.append(str(int(ip_num) & int(mask_num)))
                except ValueError:
                    network_address.append('.')

    return convert_binary_to_numbers(''.join(network_address))


def get_inverted_mask(mask_number: int) -> str:
    """
    Return inverted mask as a string.
    Inverted mask is a regular mask, where all '0'
    are changed to the '1' and vice versa.
    Return None, if the argument is not an integer.

    >>> get_inverted_mask(30)
    '00000000.00000000.00000000.00000011'
    >>> get_inverted_mask(0)
    '11111111.11111111.11111111.11111111'
    >>> get_inverted_mask(32)
    '00000000.00000000.00000000.00000000'
    >>> get_inverted_mask(-6)

    >>> get_inverted_mask('11111111.11111111.11111111.11111100')

    """
    if not isinstance(mask_number, int) or mask_number < 0:
        return None

    empty_mask = '11111111.11111111.11111111.11111111'
    return empty_mask.replace('1', '0', mask_number)


def get_broadcast_address_from_raw_address(raw_address: str) -> str:
    """
    Get and return broadcast address.
    Return None, if the argument is not a string.

    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    '91.124.230.207'
    >>> get_broadcast_address_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    binary_ip = get_binary_ip(get_ip_from_raw_address(raw_address))
    inverted_mask = get_inverted_mask(get_mask_number(raw_address))

    broadcast_address = []
    for index in range(0, 35):
        try:
            broadcast_address.append(
                str(int(binary_ip[index]) | int(inverted_mask[index])))
        except ValueError:
            broadcast_address.append('.')

    return convert_binary_to_numbers(''.join(broadcast_address))


def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    Get and return first usable ip address.
    Return None, if the argument is not a string.

    >>> get_first_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    >>> get_first_usable_ip_address_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    network_address = get_network_address_from_raw_address(raw_address)

    try:
        return network_address[:-3] + str(int(network_address[-3:]) + 1)
    except ValueError:
        return network_address[:-1] + str(int(network_address[-1]) + 1)


def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    Get and return penultimate usable ip address.
    Return None, if the argument is not a string.

    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    >>> get_penultimate_usable_ip_address_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    broadcast_address = get_broadcast_address_from_raw_address(raw_address)
    return broadcast_address[:-3] + str(int(broadcast_address[-3:]) - 2)


def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> int:
    """
    Evaluate number of usable hosts and return it as an integer.
    Return None, if the argument is not a string.

    >>> get_number_of_usable_hosts_from_raw_address('91.124.230.205/30')
    2
    >>> get_number_of_usable_hosts_from_raw_address('91.124.230.205/0')
    4294967294
    >>> get_number_of_usable_hosts_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    mask_number = get_mask_number(raw_address)
    return 2 ** (32 - mask_number) - 2


def get_ip_class_from_raw_address(raw_address: str) -> str:
    """
    Get and return ip class as a string.
    There are 5 classes: 'A', 'B', 'C', 'D', 'E'.
    Return None, if the argument is not a string.

    >>> get_ip_class_from_raw_address('91.124.230.205/30')
    'A'
    >>> get_ip_class_from_raw_address(['91', '124', '230', '205'])

    >>> get_ip_class_from_raw_address('-23.124.230.205/30')

    """
    if not isinstance(raw_address, str):
        return None

    ip_address = get_ip_from_raw_address(raw_address)
    first_octet = int(ip_address[:ip_address.find('.')])

    if 0 < first_octet <= 127:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'
    elif 240 <= first_octet <= 255:
        return 'E'
    elif first_octet <= 0:
        return None


def check_private_ip_address_from_raw_address(raw_address: str) -> bool:
    """
    Check whether an ip address is a private or not.
    Return True if it is a private and False if not.
    Return None, if the argument is not a string.

    >>> check_private_ip_address_from_raw_address('91.124.230.205/30')
    False
    >>> check_private_ip_address_from_raw_address('172.27.230.205/30')
    True
    >>> check_private_ip_address_from_raw_address(['91', '124', '230', '205'])

    """
    if not isinstance(raw_address, str):
        return None

    ip_address = get_ip_from_raw_address(raw_address)
    first_octet = int(ip_address[:ip_address.find('.')])

    if first_octet == 10:
        return True
    elif first_octet == 172:
        if 16 <= int(ip_address[4 : 6]) <= 31:
            return True
    elif first_octet == 192:
        if int(ip_address[4 : 7]) == 168:
            return True

    return False
