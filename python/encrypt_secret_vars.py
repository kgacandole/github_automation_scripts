import os
from base64 import b64encode
from nacl import encoding, public

public_key = public.PublicKey(os.environ['REPO_KEY'].encode("utf-8"), encoding.Base64Encoder())
sealed_box = public.SealedBox(public_key)
encrypted_val = sealed_box.encrypt(os.environ['SECRET_VALUE'].encode("utf-8"))

with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    print(f'repoKeyId=' + os.environ['REPO_KEY_ID'], file=fh)
    print(f'encryptedValue=' + b64encode(encrypted_val).decode('utf-8'), file=fh)
fh.close()