from PIL import Image
import os
import hashlib
from Crypto.Cipher import AES

def encrypt_file(key, input_filename, output_filename=None, chunksize=64*1024):
    if not output_filename:
        output_filename = input_filename + '.txt'
    
    vec = os.urandom(16)  # 16-byte random IV
    print(f"IV: {vec.hex()}")  # Debugging line to print the IV in hex format
    encrypter=AES.new(key, AES.MODE_CBC, vec)
    size_of_file=os.path.getsize(input_filename)

    with open(input_filename, 'rb') as infile:
        with open(output_filename, 'wb') as outfile:
            outfile.write(size_of_file.to_bytes(8, byteorder='big'))
            outfile.write(vec)
         
        
            while True:    
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encrypter.encrypt(chunk))    


def get_key(password):
    salt = b'salt_'
    AES_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return AES_key


def AES_enc():
    password = input("Enter the password: ")
    key = get_key(password)

    input_file = 'message.txt'
    output_file = 'AES_encrypted_message.enc'
    encrypt_file(key, input_file, output_file)


def LSB_enc():
    img = Image.open('image.png')
    img = img.convert('RGB')

    with open('AES_encrypted_message.enc', 'rb') as f:
        message = f.read()
    
    message_length = len(message)
    binary_length = '{0:032b}'.format(message_length)

    security_key = input("Enter security key: ")
    print("|====================================== |")
    sec_key = bytes(security_key, 'utf-8')
    bin_sec_key = ''.join(format(byte, '08b') for byte in sec_key)  # Fix binary formatting
    key_l = '{0:032s}'.format(bin_sec_key)  # Ensure 32-bit length

    binary_message = ''.join(format(byte, '08b') for byte in message)
    full_message = binary_length + key_l + binary_message
    

    print('Checking if image is large enough...')
    max_bits = img.width * img.height * 3
    if len(full_message) > max_bits:
        print("Image size is too small. Try a larger image.")
        exit()
    print(" Checked ........")
    print(" Saved ..........")
    i = 0
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(img.getpixel((x, y)))
            for j in range(3):
                if i < len(full_message):
                    pixel[j] = (pixel[j] & ~1) | int(full_message[i])  # Fix pixel modification
                    i += 1
            img.putpixel((x, y), tuple(pixel))

    img.save('hidden.png')
    print("Image saved as 'hidden.png'.")


if __name__ == '__main__':
    AES_enc()
    LSB_enc()


