"""
Commonly usable functions for the heart_slicer package.
"""
import os
import logging
from PIL import Image
import yaml

# Configure the logger
logging.basicConfig(
    level=logging.INFO)
    # format='%(asctime)s - %(name) - %(levelname) - %(message)')
logger = logging.getLogger(__name__)
# Add a file handler
fh = logging.FileHandler('logger.log')
logger.addHandler(fh)

# TODO: move use filehandles instead of opening the file in various methods
# Import the config file
def load_config(file_path):
    """Load config file."""
    logger.info(f'Loading config file: {file_path}...')
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        config['settings']['folder_input'] = os.path.realpath(config['settings']['folder_input'])
        config['settings']['folder_output'] = os.path.realpath(config['settings']['folder_output'])
    logger.info('..checking config')
    return config

CONFIG_FILE = 'config.yml'
config_path = os.path.join(os.path.dirname(__file__), '..', CONFIG_FILE)
config = load_config(config_path)

logconfig = config['logging']

# check loglevel
loglevels =  ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
if logconfig['level'] not in loglevels:
    msg = f"Not a valid logging level: {logconfig['level']}\n" + \
            f"\t\toptions are: {loglevels}"
    logger.error(msg)
    raise ValueError(msg)
# set loglevel
logger.setLevel(logconfig['level'])
# check loaded config
missing_settings = []
for key in config['settings'].keys():
    if config['settings'][key] is None:
        missing_settings.append(key)
if missing_settings != []:
    for setting in missing_settings:
        msg = f"missing value for setting: {setting}"
        logger.error(msg)
    raise ValueError(f"missing settings: {missing_settings}")
logger.info("..values for all settings provided")

# lead settings to locals
settings = config['settings']
colors = config['colors']


# check if folders exist
provided_folders = [
    'folder_input',
    'folder_output',
    'diagram_outputfolder',
]
for fld in provided_folders:
    if os.path.isdir(settings[fld]) is False:
        msg = f"Invalid value for " + \
               f"'{fld}'\n\t {settings[fld]}\n\t\tis not a valid folder "
        logger.error(msg)
        raise ValueError(msg)
logger.info("..folders exists")

logger.info("..Config checked and seems OK :)")

def logging_decorator(fn):
    """Basic logging decorator"""
    def func(*args, **kwargs):
        logger.debug(f'{fn.__name__}({args}, {kwargs})')
        return fn(*args, **kwargs)
    return func

"""
from datetime import datetime, timezone

def get_logger(log_file_name, log_sub_dir):
    log_path = f'/path/to/logs/{log_sub_dir}'
    # Create log path if it doesn't exist
    # Set up logger
    logger = logging.getLogger(log_file_name)
    logger.setLevel(logging.DEBUG)

    # Create a FileHandler and specify your own log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(f'{log_path}/{log_file_name}.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Usage example:
logger_obj = get_logger('my_function', 'my_logs')

def log_decorator(fn):
    def wrapper(*args, **kwargs):
        logger_obj.info('Enter %s', fn.__name__)
        try:
            result = fn(*args, **kwargs)
            logger_obj.info('Return value: %s', result)
            return result
        except Exception as e:
            logger_obj.error('Exception occurred: %s', e)
            raise
        finally:
            logger_obj.info('Exit %s', fn.__name__)
    return wrapper"""
##### FOR SC2 IMAGES #####
# image resolution: 40.316 pix/mm
# pixel side length = 0.024804mm
# pixel area = 0.0006152 mm2

# import time
# t1 = time.time()

@logging_decorator
def sign(x):
    """
    return the signum of x.
    edge cases not well defined
    """
    if x < 0:
        return -1
    return 1

# @logging_decorator
# def load_image(filename):
#     """
#     Load an image with Image and return the image object.
#     """
#     # TODO: not safe, use with statement to properly close file
#     return Image.open(filename)

def image_width(im):
    """
    Return the width of the image
    """
    return im.size[0]

def image_height(im):
    """
    Return the height of the image
    """
    return im.size[1]

@logging_decorator
def secs_to_str(s):
    """return string MM:SS for a given number of seconds."""
    return f"{s//60:0>2.0f}:{s%60:0>2.0f}"

@logging_decorator
def create_folder(folder):
    """
    Check if the folder exists. If it doesn't create the folder."""
    # check if folder exists
    if os.path.exists(folder):
        logger.info("..Folder already exists: "+\
                    f".\{os.path.relpath(folder, os.path.dirname(__file__))}")
    else:
        # create directory
        os.mkdir(folder)
        logger.info(f"Created folder: .\{os.path.relpath(folder, os.path.dirname(__file__))}.")


@logging_decorator
def pngs_in_fld(fld):
    """
    Return a list of all .png files in the given folder.
    """
    logger.info(os.listdir(fld))
    images_to_proces = []
    for file in os.listdir(fld):
        # check if it's a file
        filepath = os.path.join(fld, file)
        if os.path.isfile(filepath) is False:
            continue
        # check if it's a .png
        if os.path.splitext(file)[1] != '.png':
            continue
        # add to images to proces
        images_to_proces.append(file)
        if len(images_to_proces) == 0:
            logger.info(f'Found no images to in folder {fld}')
    # show result
    logger.info("found the following files:")
    for png in images_to_proces:
        logger.info(f"\t\t{png}")
    return images_to_proces

@logging_decorator
def params_from_filename(file: str, type: str) -> list:
    """
    Get the parameters from the filename. Filename should be
        heartName_sliceNr_section_resolution_abblationState_none_segmentType_SegmentNr.png
                                                                ^_segmentType_SegmentNr.png
    """
    # remove leading folders if they exist
    filename = str(os.path.split(file)[1])
    try:
        if type == "segment":
            heart, slice_nr, section, resolution, abblation_state,\
                _, segment_type, segment_nr = os.path.splitext(filename)[0].split('_')[:8]
            out = {'heart': heart,
                    "slice_nr": slice_nr,
                    "section": section,
                    "abblation_state": abblation_state,
                    "resolution": resolution,
                    "segment_nr": segment_nr,
                    "segment_type": segment_type
                    }
        if type == "slice":
            heart, slice_nr, section, resolution, abblation_state,\
                _ = os.path.splitext(filename)[0].split('_')[:6]
            out = {'heart': heart,
                    "slice_nr": slice_nr,
                    "section": section,
                    "abblation_state": abblation_state,
                    "resolution": resolution
                    }
        return out
    except ValueError as e:
        # raise InputError('not a supported file name format.')  # run calculation
        logger.info(f"Not a valid file name: {filename}\n"+\
              "images should adhere to the following naming convention:\n\t"+\
                "heartName_sliceNr_section_resolution_abblationState_none_"+\
                    "segmentType_SegmentNr.png")
        # skip this file
        raise ValueError from e


@logging_decorator
def generate_filename_segment(file_params: dict, segmentation_type: str, segment_name: str) -> str:
    """
    Generate the filename for the segment based on segment name
    and parameters from image file name.
    """
    out =  "_".join([file_params['heart'], file_params['slice_nr'], file_params['section'], file_params['resolution'], file_params['abblation_state'],\
            "out", segmentation_type, segment_name]) + ".png"
    return out
    # return f"{file_params['filename']}_{file_params['segmentation_type']}_"+\
    #         f"{segment_name}.png"
    # f"{image_file[:image_file.find('.')]}" +\
    #     f"_{segmentation_name}_{segment_names[cur_slice - 1]}.png"

@logging_decorator
def save_image(im: Image, save_folder: str, filename:str, overwrite_existing: bool) -> bool:
    """
    Save an image to the given folder and print statement to console.
    """
    # skip file if a file with the same filename exists
    if overwrite_existing is False and \
        os.path.isfile(os.path.join(save_folder, filename)) is True:
        # skip segment
        logger.info(f".skipping file: {filename}" +
            "\nalready exists in folder .\\" + \
            f"{os.path.relpath(save_folder, os.path.dirname(__file__))}.")
        return False
    # otherwise save

    im.save(os.path.join(save_folder, filename))
    logger.info(f"Saved file {filename}\n\tas: " +\
        f"{filename}\n\tin folder: .\\"+\
            f"{os.path.relpath(save_folder, os.path.dirname(__file__))}.")
    return True
