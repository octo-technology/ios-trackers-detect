import os
import sys
import shutil
import logging
from argparse import ArgumentParser
from pathlib import Path

LOG = None

def delete_directory_content(path_directory):
    """Delete all files and directories located in the argument passed path directory"""

    with os.scandir(path_directory) as entries:
        for entry in entries:
            try:
                if entry.is_dir() and not entry.is_symlink():
                    shutil.rmtree(entry.path)
                else:
                    os.remove(entry.path)
            except Exception as e:
                LOG.error('Failed to delete "{}". Reason: {}'.format(entry.path, e))
                return False

    return True

def create_directory(path_directory, empty_content_if_necessary=False):
    if path_directory.exists():
        # Directory already exists
        if empty_content_if_necessary:
            success = delete_directory_content(path_directory)
            if not success:
                return False
    else:
        path_directory.mkdir()

    return True

def init_logger():
    """Initialize script logger"""

    logger_name = Path(__file__).stem
    logger = logging.getLogger(logger_name)
    logger.setLevel(level = logging.INFO)

    formatter = logging.Formatter('%(levelname)-8s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level=logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    global LOG
    LOG = logger

def retrieve_ipa_dependencies(original_ipa_path):
    # Check if path is valid
    if not original_ipa_path.exists():
        LOG.error('IPA path "{}" does not exists on the system.'.format(original_ipa_path))
        return False

    # retrieve IPA name
    ipa_filename = original_ipa_path.stem

    # Create a new directory
    working_directory = Path.cwd()
    temp_folder_name = 'retrieve_dependencies_' + ipa_filename
    temp_folder_path = working_directory.joinpath(temp_folder_name)
    create_directory(temp_folder_path, True)

    # Copy ipa to temp folder
    ipa_path = Path(shutil.copy(original_ipa_path, temp_folder_path))

    # Change extension of the IPA file to .zip
    ipa_path_zip = ipa_path.with_suffix('.zip')
    ipa_path = ipa_path.rename(ipa_path_zip)

    # Unarchive the zip file in a temp folder
    unarchive_dest_path = temp_folder_path.joinpath(ipa_path.stem)
    shutil.unpack_archive(ipa_path, unarchive_dest_path)
    
    # Retrieve App name
    payload_path = unarchive_dest_path.joinpath('Payload')
    app_files = [fn for fn in os.listdir(payload_path) if fn.endswith('.app')]

    # Retieve Frameworks list
    frameworks_folder_path = payload_path.joinpath(app_files[0], 'Frameworks')
    LOG.info("List of dependencies found in '{}':".format(ipa_filename))
    app_dependencies = os.listdir(frameworks_folder_path)
    for dependency in app_dependencies:
        LOG.info(dependency)

if __name__ == '__main__':
    # Setup a logger for the current script to log usefull info in the console
    init_logger()

    # Retrieve script arguments
    parser = ArgumentParser(description='Retrieve Frameworks used by an IPA file')
    parser.add_argument('--ipa_path', help='path of the IPA file', required=True)
    arguments = parser.parse_args()

    ipa_path = Path(arguments.ipa_path)

    retrieve_ipa_dependencies(ipa_path)
