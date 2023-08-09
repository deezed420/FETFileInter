from cryptography.fernet import Fernet
import os, struct

class FileTypeException(Exception): pass
class FETFileOpener(): pass

class OpenFile:
    def __init__(self, path: str | bytes | os.PathLike) -> FETFileOpener:
        """
        Can open either a .fet file or a .txt file that you\n
        want to convert into a .fet file
        """

        self.path = path

    def read(self) -> str | FileTypeException:
        """
        Reads a .fet file and returns the decrypted contents\n
        if not a .fet file it will raise a FileTypeException
        """

        if os.path.splitext(self.path)[1] == '.fet':
            with open(self.path, 'b+r') as f: txt, key = f.read().strip(struct.pack('B', 0)).split(struct.pack('B', 9))
            return str(Fernet.decrypt(Fernet(key), txt))
        else: raise FileTypeException(self.path+' is not a Fernet Encrypted Text (.fet) file.')

    def write(self, text: str) -> None:
        """
        Writes the given text, turns it into Fernet Encrypted Text\n
        and then writes it to the given file
        """

        if os.path.splitext(self.path)[1] == '.fet':
            key = Fernet.generate_key()
            with open(self.path, 'b+w') as f: f.write(Fernet.encrypt(Fernet(key), text.encode())+struct.pack('B', 9)+key)
        else: raise FileTypeException(self.path+' is not a Fernet Encrypted Text (.fet) file.')
        

    def convert(self) -> None | FileTypeException:
        """
        Converts a normal .txt file to an encrypted .fet file\n
        if not a .txt file it will raise a FileTypeException
        """

        if os.path.splitext(self.path)[1] == '.txt':
            key = Fernet.generate_key()
            with open(self.path, 'b+w') as f: contents = f.read()
            open(self.path, 'w').close()
            with open(self.path, 'b+w') as f: f.write(Fernet(key).encrypt(contents)+struct.pack('B', 9)+key)
            os.rename(self.path, os.path.splitext(self.path)[0]+'.fet')
        else: raise FileTypeException(self.path+' is not a Plain Text (.txt) file.')
        