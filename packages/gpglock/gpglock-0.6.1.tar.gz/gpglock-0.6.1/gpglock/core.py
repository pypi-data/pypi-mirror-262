#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import gnupg
import hashlib
import os
import subprocess
from .utils.console_logging_formatter import get_formatted_console_logger

logger = get_formatted_console_logger("gpglocker")


def __is_dir_inited(dir_path):
    config_path = os.path.join(dir_path, ".gpglock")
    return os.path.isfile(config_path)


def __digest_binary_hash(data):
    return hashlib.sha1(data).hexdigest()


def __digest_file_hash(filepath):
    with open(filepath, "rb") as opened_file:
        return __digest_binary_hash(opened_file.read())


def __encrypt_file(gpg, filepath, recipient):
    stream = open(filepath, "rb")
    res = gpg.encrypt_file(stream, recipient, armor = False)

    if not res.ok:
        raise AssertionError("GPG error: %s, output: %s" % (res.status, res.stderr))

    return res.data


def __decrypt_file(gpg, filepath):
    stream = open(filepath, "rb")
    res = gpg.decrypt_file(stream)

    if not res.ok:
        raise AssertionError("GPG error: %s, output: %s" % (res.status, res.stderr))

    return res.data


def __lock_file(gpg, dir, clear_file, recipient):
    clear_file_realpath = os.path.realpath(os.path.join(dir, clear_file))
    encrypted_file = "%s.gpg" % clear_file
    encrypted_file_realpath = "%s.gpg" % clear_file_realpath

    if not os.path.isfile(clear_file_realpath):
        logger.warning("The file to encrypt doesn't exist: %s" % clear_file)
        return

    if os.path.isdir(encrypted_file_realpath):
        raise AssertionError("Invalid path to encrypt: %s" % encrypted_file)

    if os.path.isfile(encrypted_file_realpath):
        existing_data = __decrypt_file(gpg, encrypted_file_realpath)
        existing_hash = __digest_binary_hash(existing_data)
        pending_hash = __digest_file_hash(clear_file_realpath)
        if pending_hash == existing_hash:
            # delete the clear file
            os.remove(clear_file_realpath)
            logger.info("No content change: %s" % clear_file)
            return

    # encryption and write to target path
    encrypted_data = __encrypt_file(gpg, clear_file_realpath, recipient)
    with open(encrypted_file_realpath, "wb") as target_file:
        target_file.write(encrypted_data)

    # delete the clear file
    os.remove(clear_file_realpath)
    logger.info("Locked %s" % clear_file)


def __unlock_file(gpg, dir, clear_file):
    clear_file_realpath = os.path.realpath(os.path.join(dir, clear_file))
    encrypted_file = "%s.gpg" % clear_file
    encrypted_file_realpath = "%s.gpg" % clear_file_realpath

    if not os.path.isfile(encrypted_file_realpath):
        logger.warning("Invalid file to decrypt: %s" % encrypted_file)
        return

    if os.path.isdir(clear_file_realpath):
        raise AssertionError("Invalid path to decrypt: %s" % clear_file)

    clear_data = __decrypt_file(gpg, encrypted_file_realpath)

    with open(clear_file_realpath, "wb") as target_file:
        target_file.write(clear_data)
    logger.info("Unlocked %s" % clear_file)


def __get_gpg_info():

    gpg_home = None
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
            "Failed loading default recipient, please add [default-recipient email-address] to [gpg.conf] in [%s]."
            % gpg_home
        )

    return {"gpgHome": gpg_home, "defaultRecipient": default_recipient}


def __ensure_valid_dir(dir_path):
    if not os.path.exists(dir_path):
        raise AssertionError("Directory does not exist: %s" % dir_path)

    if os.path.isfile(dir_path):
        raise AssertionError(
            "Invalid input, the given path is not a directory but a file: %s" % dir_path
        )


def __load_entities(dir_path):

    gpglock_path = os.path.join(dir_path, ".gpglock")
    if not os.path.exists(gpglock_path):
        raise AssertionError(
            "The directory has not been initialised, run [gpginit] first."
        )

    res = []
    with open(gpglock_path, "r") as config_file:
        lines = config_file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            res.append(line)

    return res


def init_dir(dir_path):

    # init
    __ensure_valid_dir(dir_path)
    __get_gpg_info()

    if __is_dir_inited(dir_path):
        raise AssertionError("Current working directory is already initialised.")

    TEMPLATE = """# List secret files which need to be locked below.

# example:
# ./secret.txt
# ./sub-folder/token.conf
# ...

"""

    gpglock_path = os.path.join(dir_path, ".gpglock")
    with open(gpglock_path, "w") as config_file:
        config_file.write(TEMPLATE)

    logger.info(
        "Init succeeded, check [.gpglock] and add secret files to later lock them."
    )


def lock_dir(dir_path):

    # init
    __ensure_valid_dir(dir_path)
    entities = __load_entities(dir_path)
    gpg_info = __get_gpg_info()

    gpg = gnupg.GPG()
    gpg.encoding = "utf-8"

    if not len(entities):
        logger.info("No specific file to lock.")
        return

    for entity in entities:
        __lock_file(gpg, dir_path, entity, gpg_info["defaultRecipient"])


def unlock_dir(dir_path):

    # init
    __ensure_valid_dir(dir_path)
    entities = __load_entities(dir_path)
    __get_gpg_info()

    gpg = gnupg.GPG()
    gpg.encoding = "utf-8"

    if not len(entities):
        logger.info("No specific file to unlock.")
        return

    for entity in entities:
        __unlock_file(gpg, dir_path, entity)
