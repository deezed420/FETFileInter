from cryptography.fernet import Fernet
import os, struct

class FileException(Exception): pass
class FETFileOpener(str): pass

class OpenFile:
    def __init__(self, path) -> FETFileOpener:
        """
        Can open either a .fet file or a .txt file that you\n
        want to convert into a .fet file
        """

        self.path = path

    def read(self) -> str | FileException:
        """
        Reads a .fet file and returns the decrypted contents\n
        if not a .fet file it will raise a FileException
        """

        if os.path.splitext(self.path)[1] == '.fet':
            txt, key = os.read(os.open(self.path, os.O_RDONLY), 1000000).strip(struct.pack('B', 0)).split(struct.pack('B', 9))
            return str(Fernet.decrypt(Fernet(key), txt))
        else: raise FileException(self.path+' is not a Fernet Encrypted Text (.fet) file.')
            
    
    def convert(self) -> None | FileException:
        """
        Converts a normal .txt file to an encrypted .fet file\n
        if not a .txt file it will raise a FileException
        """

        if os.path.splitext(self.path)[1] == '.txt':
            f=os.open(self.path, os.O_RDWR)
            key = Fernet.generate_key()
            contents = os.read(f, 1000000)

            open(self.path, 'w').close()
            os.write(f, Fernet(key).encrypt(contents)+struct.pack('B', 9)+key) ; os.close(f)
            os.rename(self.path, os.path.splitext(self.path)[0]+'.fet')
        else: raise FileException(self.path+' is not a Plain Text (.txt) file.')