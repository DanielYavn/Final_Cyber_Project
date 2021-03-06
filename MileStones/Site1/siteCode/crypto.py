from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
import os, random, base64


def encrypt(path):
    """
    encrypt game
    :param path:game path
    :return: dictionary with cryto keys
    """
    choice = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = ''.join(random.choice(choice) for m in xrange(32))
    iv = ''.join(random.choice(choice) for m in xrange(16))

    epath = os.path.abspath("./siteCode/egames/" + "e" + os.path.split(path)[-1])

    with open(path, "rb") as inf:
        aes = AES.new(key, AES.MODE_CBC, iv)
        encoder = PKCS7Encoder()

        text = inf.read()
        if len(text) % 16 == 0:
            text += "A_PADDING_FIXER"

        # pad the plain text according to PKCS7
        pad_text = encoder.encode(text)
        # encrypt the padding text
        cipher = aes.encrypt(pad_text)

        # base64 encode the cipher text for transport
        enc_cipher = base64.b64encode(cipher)

        with file(epath, "wb") as outf:
            outf.write(enc_cipher)

    return {"key": unicode(key), "iv": unicode(iv), "encrypted_code_path": epath}


def no_encryption(path):  # not encrypting

    epath = os.path.abspath("./siteCode/egames/" + "e" + os.path.split(path)[-1])

    with open(path, "rb") as inf:

        text = inf.read()

        # base64 encode the cipher text for transport
        enc_cipher = base64.b64encode(text)

        with file(epath, "wb") as outf:
            outf.write(enc_cipher)

    return {"key": unicode(0), "iv": unicode(0), "encrypted_code_path": epath}
