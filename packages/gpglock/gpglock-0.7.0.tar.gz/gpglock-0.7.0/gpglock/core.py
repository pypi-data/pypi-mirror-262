#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from gpglock.utils.file_system import get_all_non_hidden_files
from gpglock.utils.gpg_wrapper import get_gpg_info, gpg_decrypt_to_bytes, gpg_decrypt_to_file, gpg_encrypt_to_file
from gpglock.utils.console_logging_formatter import get_formatted_console_logger
from gpglock.utils.hash import sha1_digest_bytes, sha1_digest_file

logger = get_formatted_console_logger("gpglocker")


def __is_dir_inited(dir_path):
    config_path = os.path.join(dir_path, ".gpglock")
    return os.path.isfile(config_path)

def __is_same(raw_file:str, encrypted_file:str)->bool:
    hash1 = sha1_digest_file(raw_file)
    hash2 = sha1_digest_bytes(gpg_decrypt_to_bytes(encrypted_file))
    return hash1 == hash2

def __ensure_valid_dir(dir_path):
    if not os.path.exists(dir_path):
        raise AssertionError("Directory does not exist, path: [%s]" % dir_path)

    if os.path.isfile(dir_path):
        raise AssertionError(
            "The given path is not a directory but a file: [%s]" % dir_path
        )


def init_dir(dir_path):

    # init
    __ensure_valid_dir(dir_path)
    get_gpg_info()

    if __is_dir_inited(dir_path):
        raise AssertionError("Current working directory is already initialised.")

    TEMPLATE = """# The gpglock CLI application lock & unlocks files in this directory and its sub directories."""

    gpglock_path = os.path.join(dir_path, ".gpglock")
    with open(gpglock_path, "w") as config_file:
        config_file.write(TEMPLATE)

    logger.info(
        "gpglock inited, now you can lock and unlock files in this directory  and its sub directories."
    )


def lock_dir(dir_path):
    # init
    __ensure_valid_dir(dir_path)
    if not __is_dir_inited(dir_path):
        logger.warn("Directory [%s] is not initialised, please run [gpginit] first" % dir_path)    
        return
    gpg_info = get_gpg_info()

    all_files = get_all_non_hidden_files(dir_path)
    raw_files = [e for e in all_files if not e.endswith('.gpg')]
    
    if not len(raw_files):
        logger.info("No file to lock.")
        return

    for raw_file in raw_files:
        encrypted_file = raw_file+'.gpg'
        if os.path.exists(encrypted_file) and __is_same(raw_file, encrypted_file):
            logger.warn("No change, skip %s" % encrypted_file)
        else:
            gpg_encrypt_to_file(raw_file, gpg_info["defaultRecipient"])
            logger.info("Locked %s" % encrypted_file)
        os.remove(raw_file)


def unlock_dir(dir_path):
    # init & verify
    __ensure_valid_dir(dir_path)
    if not __is_dir_inited(dir_path):
        logger.warn("Directory [%s] is not initialised, please run [gpginit] first" % dir_path)    
        return
    get_gpg_info()

    # index encrypted files
    all_files = get_all_non_hidden_files(dir_path)
    encrypted_files = [e for e in all_files if e.endswith('.gpg')]

    if not len(encrypted_files):
        logger.info("No file to unlock.")
        return

    for encrypted_file in encrypted_files:
        decrypted_file = encrypted_file[0:len(encrypted_file)-4]
        if os.path.isdir(decrypted_file):
            raise AssertionError("Target file path %s is a directory" % decrypted_file)
        gpg_decrypt_to_file(encrypted_file, decrypted_file)
        logger.info("Unlocked %s" % decrypted_file)
        os.remove(encrypted_file)
