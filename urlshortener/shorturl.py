'''Utilities for shortening the URL'''


ALPHABET = 'Ods743kTSxYLboCaVNFQM9pwJH8hvGyI0tEqnKAXDzlr1ZPiugBU65fRmjeW2c'


def encode(number, alphabet=ALPHABET):
    '''Encode number in base(len(alphabet)) encoding'''
    n = len(alphabet)
    encoding = []
    while number > 0:
        number, mod = divmod(number, n)
        encoding.append(alphabet[mod])
    return ''.join(encoding)


def mix_number(number, block_size=16):
    '''Swap lower and higher block_size number bits'''
    lower_mask = (1 << block_size) - 1
    upper_mask = (1 << 2 * block_size) - 1
    return (((number & lower_mask) << block_size) | 
                ((number & upper_mask) >> block_size))
