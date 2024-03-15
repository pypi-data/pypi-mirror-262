import subprocess
import os
from typing import List

def __open_subprocess(args: List[str]) -> bytes:
    gpg = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = gpg.communicate()
    if gpg.returncode == 0:
        return stdout
    else:
        error = stderr.decode('utf-8')
        raise ChildProcessError(error)

def get_gpg_info():
    gpg_home = None
    gpg_conf = None
    default_recipient = None
    try:
        gpg = subprocess.Popen(["gpg", "--version"], stdout=subprocess.PIPE)
        output = gpg.communicate()[0].decode("ascii")
        for line in output.split("\n"):
            if line.startswith("Home:"):
                gpg_home = line[6:]
                gpg_conf = os.path.join(gpg_home, "gpg.conf")
                with open(gpg_conf) as gog_conf_file:
                    for line in gog_conf_file.readlines():
                        keypair = line.strip().split(" ")
                        if len(keypair) != 2:
                            continue
                        key = keypair[0].strip()
                        if key == "default-recipient":
                            default_recipient = keypair[1].strip()
                            break
    except FileNotFoundError as e:
        pass

    if not gpg_home:
        raise AssertionError("Failed fetching gpg home, make sure gpg is installed.")

    if not default_recipient:
        raise AssertionError(
            "Failed loading default recipient, please add [default-recipient email-address] to [%s]."
            % (gpg_conf)
        )

    return {"gpgHome": gpg_home, "defaultRecipient": default_recipient}

def gpg_encrypt_to_file(input_filepath:str, recipient:str):
    return __open_subprocess(["gpg", "--encrypt", "--batch", "--yes", "--quiet", "--recipient", recipient, input_filepath])

def gpg_decrypt_to_file(input_filepath:str, output_filepath:str):
    __open_subprocess(["gpg", "--decrypt", "--batch", "--yes", "--quiet", "--output", output_filepath, input_filepath])

def gpg_decrypt_to_bytes(input_filepath:str) -> bytes:
    return __open_subprocess(["gpg", "--decrypt", "--batch", "--yes", "--quiet", input_filepath])
