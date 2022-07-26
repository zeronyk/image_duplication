import argparse
from genericpath import isfile
import logging
import os
import sys
import time
import itertools
import os_functions
import constants
import duplication_functions

def main(path1:list, path2:list, csv = None, delete = False, t = False, ts = 100, lvl = 1, remove_others = False):
    
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare path2 to path1 and find all image duplicates listed in path1 and path2.')
    
    
    
    parser.add_argument('path1', metavar='path1', type=str, nargs='+',
                        help='original path or list of paths')
    parser.add_argument('path2', metavar='path2',type=str, nargs='+',
                        help='path to check and optinal delete duplicates in')

    parser.add_argument("-l", "--log-file",type=str, help="path of the log file to be written, defaults to duplicates.log in current folder")
    parser.add_argument("-o", "--output-csv", type=str, help="ouputs csv list of duplicates")
    parser.add_argument("-d", "--delete", action='store_true', help="automatically deletes duplicates")
    #parser.add_argument("-c", "--copy", nargs="+", type=str, help="copy non duplicate files from path2 to this path")
    parser.add_argument("-t", "--threading", action='store_true', help="use multithreading to help speedup the process")
    #parser.add_argument("-a", "--all", action='store_true', help="Consider all Pictures to be potential duplicates (else only consider pictures with same name, significantly reduces runtime)")
    parser.add_argument("-ts", "--imagehash-threshold",type=int, default = 100,help = "if not used -a how much simularity must be on the imagehash of the pictues (values will be interpreted as percent) default is 100")
    parser.add_argument("-rem", "--remove-other", action='store_true', help = "removes other files, that are not considerd documents (good if there is a lot of junk) only works with -d")
    parser.add_argument("-lvl", "--directory-level", type=int, default=1, help = "level of depth in namematching to be used while syntax finding duplicates (lvl= 0: consider every file, lvl=1: consider onlye files with same name, lvl=2: consider only files with same named subfolder and same filename), default is 1")
    args = parser.parse_args()
    
    
    # handle logging
    if args.log_file:
        try:
            logging.basicConfig(
                        handlers=[
                            logging.FileHandler(args.log_file),
                            logging.StreamHandler(sys.stdout)
                        ],
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

        except Exception as e:
            print(f"Logging threw error {e}")
            raise e
    else:
        try:
            logging.basicConfig(
                        handlers=[
                            logging.FileHandler("duplicates.log"),
                            logging.StreamHandler(sys.stdout)
                        ],
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

        except Exception as e:
            print(f"Logging threw error {e}")
            raise e


    # Errorchecking paths
    if not (isinstance(args.path1, list) or isinstance(args.path1, str)):
        logging.error("path1 is no list nor a string, please fix path1") 
        raise Exception("Malformed path1, please insert string or list of strings")

    for path in args.path1:
        if os.path.isfile(path) or not os.path.exists(path):
            logging.error("Path1 does contain files or reference path that does not exist") 
            raise Exception("Path1 does contain files or reference path that does not exist")
    
    for path in args.path2:
        if os.path.isfile(path) or not os.path.exists(path):
            logging.error("Path2 does contain files or reference path that does not exist") 
            raise Exception("Path2 does contain files or reference path that does not exist")

    if not (isinstance(args.path2, list) or isinstance(args.path2, str)):
        logging.error("path2 is no list nor a string, please fix path2")
        raise Exception("Malformed path2, please insert string or list of strings")
    
    # can we open the output list ?
    csv = None
    if args.output_csv:
        if os_functions.check_output_list(args.output_csv):
            logging.info("Passed check for writability of outputlist")
        else:
            logging.info("Ouputlist is not writable, you will need to privelege this user")
            if os_functions.prompt_sudo() != 0:
                logging.error("Need super user privleges to continue")
            if not os_functions.check_output_list(args.output_csv):
                logging.error("Priveleged root user can not write file, please fix output_csv issue")
                raise Exception("Error while checking for write priveleges on ouput_list, check logging for error discription")
        csv = args.output_csv


    logging.info(f"Starting new run with path1 {args.path1} and path2 {args.path2}")
    if not os_functions.check_sudo():
        answer = os_functions.query_yes_no('Continue as underpivileged user might cause problems later in the program, you want to privlege this process ?')
        if answer:
            os_functions.prompt_sudo()
    if args.remove_other: 
        logging.info(f"remove-others was choosen whitelisted formats that won't be deleted are {constants.whitelist_formats}.")

    start = time.time()
    main(args.path1, args.path2, csv = csv, delete = args.delete, t = args.threading, ts= 100, lvl = int(args.directory_level), remove_others = False )
    logging.info(f"Process was finisehd in {time.time()- start}s")


