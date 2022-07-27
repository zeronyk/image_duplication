# checks for su probably needed to delete!
import os, subprocess
import sys
import logging
import threading
from typing import final

# promts sudo and leverage priveleges
def prompt_sudo():
    ret = 0
    if os.geteuid() != 0:
        msg = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
    return ret

# chekcs for root
def check_sudo():
    if os.geteuid() != 0:
        return False
    else:
        return True
        
        
# check if file can be created, creates header of csv file 
def check_output_list(csv_path):
    try:
        with open(csv_path, "a") as f:
            f.write("duplicate;duplicate_from\n")
        logging.info("Passed write test of ouput_list")
    except Exception as e:
        logging.error(f'Opening file {csv_path} threw exception {str(e)}!')
        return False
    return True

#https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def remove_formats_not_in_list(path, format_list):
    counter = 0
    for p in path:
        for root, dirs, files in os.walk(p, topdown=False):
            for file in files:
                if not file.lower().endswith(format_list):
                    os.remove(os.path.join(root,file))
                    counter = counter+1
        logging.info(f"Removed {counter} files in folder {p}")

def get_files(path, endings):
    output_list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            if file.lower().endswith(endings):
                output_list.append((root, file))
    return output_list

class del_thread(threading.Thread):
    
    def __init__(self, name, chunk):
        threading.Thread.__init__(self)
        self.name = name
        self.chunck = chunk
    
    def run(self):
        logging.info(f"Thread {self.name} started with {len(self.chunck)} images to delete")
        for i,path in enumerate(self.chunck):
            try:
                if os.path.isfile(path):
                    os.remove(path)

                if i % 1000 == 0:
                    logging.info(f"reached {i}/{len(self.chunck)} at {(i/len(self.chunck)) * 100}%")
            except Exception as e:
                logging.warn(f"del_list in thread {self.name} encounterd an error {str(e)} continue...")
            finally:
                continue
        logging.info(f"Thread {self.name} finished and deleted {len(self.chunck)} files")

def del_list_threaded(duplicates: list):
    number_of_cores = os.cpu_count()
    logging.info(f"Starting deletion on {number_of_cores} threads")
    splitted_list = list(split(duplicates, number_of_cores))
    threads = []
    for x in range(number_of_cores):
        threads.append(del_thread(x, splitted_list[x]))
        
    for t in threads:
        t.start()
    # thanks to GIL this should make any difference to sequential version
    for t in threads:
        t.join()

    logging.info(f"Finished multithreaded deletion!")
    return

# removes all paths in list
def del_list(path_list):
    for i,path in enumerate(path_list):
        try:
            if os.path.isfile(path):
                os.remove(path)

            if i % 1000 == 0:
                logging.info(f"reached {i}/{len(path_list)} at {(i/len(path_list)) * 100}%")
        except Exception as e:
            logging.warn(f"del_list encounterd an error {str(e)} continue...")
        finally:
            continue

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))