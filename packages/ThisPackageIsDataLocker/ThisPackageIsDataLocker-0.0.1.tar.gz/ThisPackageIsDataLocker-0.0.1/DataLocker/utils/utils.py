def read_file(path, block_size=None):

    with open(path, 'rb') as file:
        
        if block_size:
            return file.read(block_size), file.read()

        return file.read()


def write_file(path, content, cipher_iv=None):

    with open(path, 'wb') as file:

        if cipher_iv:
            file.write(cipher_iv)

        file.write(content)
