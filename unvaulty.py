"""
This program "decrypts" files that were saved in a Vaulty vault. 
No password is needed to decrypt, as the files are not actually encrypted.
The filetypes are obscured, so decrypted files are temporarily moved to a 
"Staging" directory to detect the filetype using `mimetypes`. 

Usage: Change the "DIRECTORIES_TO_DECRYPT" to include the directory with all
of your .vaulty files. Then run `python unvaulty.py`

See vaultyapp.com for the app that created these secure files.
"""
import os
import mimetypes
mimetypes.init()

STAGING_DIRECTORY = 'STAGING/'
DECRYPTED_DIRECTORY = 'DECRYPTED/'
DIRECTORIES_TO_DECRYPT = ['data/', 'temp/']

for directory in [STAGING_DIRECTORY, DECRYPTED_DIRECTORY]:
    if not os.path.exists(directory):
        os.mkdir(directory)

def parse(filename, directory, new_directory = STAGING_DIRECTORY):
    with open(directory + filename, 'rb') as old_file:
        if not filename.endswith('.vdata'):
            # FILE IS ALREADY DECRYPTED, PASS
            return
        data = old_file.read()
        # REMOVE 'obscured' FROM BEGINNING OF FILE IF IT'S A PICTURE FILE
        if data[:8] == b'obscured':
            # EXACT FILETYPE WILL BE DETECTED LATER
            extension = '.jpg'
        else:
            # VIDEO FILES ARE NOT 'obscured'
            extension = '.mp4'

        # WRITE TO NEW FILE
        new_filename = filename.split('.')[0] + extension
        #print("New filename:%s" % new_filename)
        with open(new_directory + new_filename, 'wb') as new_file:
            new_file.write(data[8:])

for directory in DIRECTORIES_TO_DECRYPT:
    for file in os.listdir(directory):
        parse(file, directory)

MAGIC_BYTES = {b'\xff\xd8\xff\xe0': '.jpg', # JPG without EXIF
               b'\xff\xd8\xff\xe1': '.jpg', # JPG with EXIF
               b'\xff\xd8\xff\xe2': '.jpg',
               b'\xff\xd8\xff\xe3': '.jpg',
               b'\xff\xd8\xff\xe8': '.jpg',
               b'\xff\xd8\xff\xc0': '.jpg', # DON'T KNOW WHY THIS IS JPG...
               b'BM\xde\x01': '.bmp',
               b'GIF8': '.gif',
               b'\x89\x50\x4e\x47': '.png'
               }

EXTENSIONS = {'image/jpeg': '.jpg',
              'video/mp4': '.mp4'
              }

for file_name in os.listdir(STAGING_DIRECTORY):
    file_path = STAGING_DIRECTORY + file_name
    guessed_type = mimetypes.guess_type(file_path)[0]
    if guessed_type in EXTENSIONS:
        file_type = EXTENSIONS[guessed_type]
    else:
        print("COULD NOT DETECT FILE TYPE FOR FILE {0}!".format(file_path))
        continue
    
    with open(file_path, 'rb') as renamed_file:
        first_bytes = renamed_file.read(4)

    if first_bytes not in MAGIC_BYTES and file_type == '.mp4':
        # IF IT'S A VIDEO FILE, IT WILL PROBABLY PLAY JUST FINE ANYWAY...
        new_file_extension = '.mp4'
    
    elif first_bytes in MAGIC_BYTES:
        new_file_extension = MAGIC_BYTES[first_bytes]
    else:
        print("COULD NOT DETERMINE FILE TYPE!")
        hex_bytes = ':'.join('{:02x}'.format(c) for c in first_bytes)
        print("FILE MAGIC BYTES: {0}".format(hex_bytes))
        continue
    
    corrected_filename = file_without_extension + new_file_extension
    file_without_extension, _ = file_name.split('.')
    final_path = DECRYPTED_DIRECTORY + corrected_filename
    # MOVE THE BEST GUESS FILE TO THE DECRYPTED DIRECTORY
    os.rename(file_path, final_path)    

    
