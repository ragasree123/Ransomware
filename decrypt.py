from Crypto.Cipher import AES
import os

def decrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        original_size = int.from_bytes(infile.read(8), 'big')
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(original_size)
   
    os.remove(in_filename)  # Delete the .enc file after decryption

def decrypt_directory(key, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.enc'):
                full_file_path = os.path.join(root, file)
                decrypt_file(key, full_file_path)
                # The .enc file will be deleted in the decrypt_file function after decryption

with open("key.bin", "rb") as keyfile:
    key = keyfile.read()  # Load the key from the same file

decrypt_directory(key, "critical")  # Decrypt files in the directory
