import argparse
import logging
import os
import sys
import time
import image_duplicate_finder.os_functions as os_functions
import image_duplicate_finder.constants as constants
import image_duplicate_finder.duplication_functions as duplication_functions

def find_dups(path1 : list, path2:list, csv = None, delete = False, t = False, ts = 100, lvl = 1, remove_others = False):
    
    if not delete and remove_others:
        logging.error("Remove others is called without delte. Please procede with caution, remove others will remove a lot of files in path1 and path2, if you only want to delete pictueres only use -d")
        raise Exception("Remove others was called without -d flag")

    if remove_others:
        answer =os_functions.query_yes_no(f"Are you sure you want to delete all not whitelisted files {constants.whitelist_formats} in {path1} AND {path2}")
        if answer:
            logging.info("Removing others is True, now start delteing not whitelisted_formats")
            for path in path1:
                os_functions.remove_formats_not_in_list(path1, constants.whitelist_formats)
            for path in path2:
                os_functions.remove_formats_not_in_list(path2, constants.whitelist_formats)
        else: 
            logging.error("Arguments were used wrong, please read -h for help")
            raise Exception("You were close to deleting maybe important files, please read -h")
    path1_list = []
    for path in path1:
        path1_list.extend(os_functions.get_files(path, constants.picture_formats))
    
    logging.info(f"Found {len(path1_list)} pictures in {path1}")
    path2_list = []
    for path in path2:
        path2_list.extend(os_functions.get_files(path, constants.picture_formats))
    
    logging.info(f"Found {len(path1_list)} pictures in {path2}")
    # syntactic duplicate checking
    possible_duplicates = duplication_functions.find_duplicates_by_name(path1_list, path2_list, lvl)
    # semantic dupcliate checking
    # with or without threading
    if t:
        deletion_list = duplication_functions.find_duplicates_semantic_threaded(possible_duplicates, ts=ts, csv = csv)

    else:
        deletion_list = duplication_functions.find_duplicates_semantic(possible_duplicates, ts=ts, csv = csv)
    if delete:
        if t:
            os_functions.del_list_threaded(deletion_list)
        else:
            os_functions.del_list(deletion_list)
    return



