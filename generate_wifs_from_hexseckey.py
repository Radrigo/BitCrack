#!/usr/bin/env python3

import bitcoin
import argparse


def cmdline_args():
    p = argparse.ArgumentParser(description=
        """
            Wifs BTC creator        
        """, 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('HexSecKey', help=None,
                   nargs=None, const=None, default=None,
                   type=None, choices=None, metavar=None)
    p.epilog = None
    return p.parse_args()

args = cmdline_args();

# Generate a random private key
valid_private_key = False
while not valid_private_key:
    if args.HexSecKey:
        private_key = args.HexSecKey
    else:
        private_key = bitcoin.random_key()
    decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
    valid_private_key =  0 < decoded_private_key < bitcoin.N

print("Private Key (hex): ", private_key)
# print("Private Key (decimal) is: ", decoded_private_key) // TODO VERBOSE

# Convert private key to WIF format
wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
print("Private Key (WIF): ", wif_encoded_private_key)

# Add suffix "01" to indicate a compressed private key
compressed_private_key = private_key + '01'
# print("Private Key Compressed (hex) is: ", compressed_private_key) // TODO VERBOSE

# Generate a WIF format from the compressed private key (WIF-compressed)
wif_compressed_private_key = bitcoin.encode_privkey(
    bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif')
print("Private Key (WIF-Compressed): ", wif_compressed_private_key)

# Multiply the EC generator point G with the private key to get a public key point
public_key = bitcoin.multiply(bitcoin.G, decoded_private_key)
# print("Public Key (x,y) coordinates is:", public_key) // TODO VERBOSE

# Encode as hex, prefix 04
hex_encoded_public_key = bitcoin.encode_pubkey(public_key,'hex')
# print("Public Key (hex) is:", hex_encoded_public_key) // TODO VERBOSE

# Compress public key, adjust prefix depending on whether y is even or odd
(public_key_x, public_key_y) = public_key
if (public_key_y % 2) == 0:
    compressed_prefix = '02'
else:
    compressed_prefix = '03'
hex_compressed_public_key = compressed_prefix + bitcoin.encode(public_key_x, 16)
# print("Compressed Public Key (hex) is:", hex_compressed_public_key) // TODO VERBOSE

# Generate bitcoin address from public key
print("Bitcoin Address (b58check): ", bitcoin.pubkey_to_address(public_key))

# Generate compressed bitcoin address from compressed public key
print("Compressed Bitcoin Address (b58check): ", \
    bitcoin.pubkey_to_address(hex_compressed_public_key))
