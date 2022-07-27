import os
import logging
import threading
import imagehash
from PIL import Image

import image_duplicate_finder.os_functions as os_functions
import image_duplicate_finder.constants as constants


# finds duplicates by name and lvl (lvl= 0: consider every file, lvl=1: consider onlye files with same name, lvl=2: consider only files with same named subfolder and same filename)
# returns list(tuple) where tuple is (path1, path2) for every duplicate
def find_duplicates_by_name(path_list1, path_list2, lvl):
    if lvl > 2 or lvl < 0:
        logging.info(f"lvl parameter was set wrongly, can only be one of [0,1,2] but was {lvl}")
        raise Exception(f"lvl parameter was set wrongly, can only be one of [0,1,2] but was {lvl}")

    
    if lvl == 0:
        raise Exception("Not implemented")
        logging.warn("Using lvl 0 can result in bad results, since path1 won't be checked against path1 and path2 visa versa")
        # p1 x p1 (without id)
        # p2 x p2 (without id)
        # p1 x p2
        duplicates = []
        
        # cool method but is making mistakes
        #duplicates.extend([(x,y) for x, y in filter(lambda x: x[0] != x[1], itertools.product(path_list1, path_list1))])
        #duplicates.extend([(x,y) for x, y in filter(lambda x: x[0] != x[1], itertools.product(path_list2, path_list2))])
        #duplicates.extend(list(itertools.product([os.path.join(x[0], x[1]) for x in path_list1], [os.path.join(x[0], x[1]) for x in path_list2])))
        
        
        logging.info(f"Found {len(duplicates)} syntactic duplicates, by level {lvl}")
        return duplicates
    
    if lvl == 1:
        # https://stackoverflow.com/questions/22386287/python-get-item-from-set-based-on-key
        # thanks to this we know that dict are also implemented as hash table and therefore should have "in" questions in avg O(1)
        # we wont use sets even if they should be really really really good here ...

        duplicates = []
        unique_dict = {}
        # check for duplicates in name_list1
        for path, name in path_list1:
            if not name in unique_dict:
                unique_dict[name] = os.path.join(path, name)
            else:
                duplicates.append((unique_dict[name], os.path.join(path, name)))
            
        logging.info("Finished finding duplicates in first list")
        # check for dupliates in name_list2
        for path, name in path_list2:
            if not name in unique_dict:
                unique_dict[name] = os.path.join(path, name)
            else:
                duplicates.append((unique_dict[name], os.path.join(path, name)))
        
        # duplicates is orderd first there are path1 vs path1 then there are path1 vs path2 so on the "right side" of the tuple there should be path2 wherever possible
        logging.info(f"Found {len(duplicates)} syntactic duplicates, by level {lvl}")
        return duplicates

    
    
    logging.info(f"Syntax name finding duplicates is set to {lvl}, (lvl= 0: consider every file, lvl=1: consider onlye files with same name, lvl=2: consider only files with same named subfolder)")
    if lvl == 2:
        logging.log(f"lvl 2 is currently not supported please open an issue!")
        raise Exception(f"lvl 2 is currently not supported please open an issue!")
        #name_list1 = [os.path.join(os.path.basename(os.path.normpath(x[0]) for x in path_list1] somthing like this
    
def write_tuple_list_to_csv(path, list):
    with open(path, "a") as f:
        f.writelines([f"{x[0]}, {x[1]}\n" for x in list])
    logging.info(f"Finisehd writing duplicates into csv file {path}")
           

# make an image hashing for semantic duplication detection
# returns list to delete
def find_duplicates_semantic(duplicates: list, ts, csv = None):
    logging.info(f"Starting semantic evaluation singlethreaded")
    deletion_list = []
    for i,(path1, path2) in enumerate(duplicates):
        try:
            hash0 = imagehash.average_hash(Image.open(path1)) 
            hash1 = imagehash.average_hash(Image.open(path2)) 
            if hash0 - hash1 <= 100 - ts:
                deletion_list.append((path1,path2))
            if i % 1000 == 0:
                logging.info(f"Reached {i}/{len(duplicates)} at {(i/len(duplicates)) * 100}%")
        except Exception as e:
            logging.warn(f"Imagehash encounterd an error {str(e)} skipping and continue")
        finally:
            continue
    if csv:
        write_tuple_list_to_csv(path=csv, list = deletion_list)
    logging.info(f"Found {len(deletion_list)} elements for deletion")
    return [x[1] for x in deletion_list]


# checks two paths on imagehash equality
def hash_image_on_ts(path1, path2, ts):
    try:
        hash0 = imagehash.average_hash(Image.open(path1)) 
        hash1 = imagehash.average_hash(Image.open(path2)) 
        if hash0 - hash1 <= 100 - ts:
            return True
        else:
            return False
    except Exception as e:
        logging.warn(f"Imagehash encounterd an error {str(e)} skipping and continue")

class img_hash_thread(threading.Thread):
    
    def __init__(self, name, chunk, ts):
        threading.Thread.__init__(self)
        self.name = name
        self.chunck = chunk
        self.ouput_list = []
        self.ts = ts
    
    def run(self):
        logging.info(f"Thread {self.name} started with {len(self.chunck)} images to compare")
        deletion_list = []
        for i, (p1, p2) in enumerate(self.chunck):
            if hash_image_on_ts(p1,p2,self.ts):
                deletion_list.append((p1,p2))
            if i % 1000 == 0:
                logging.info(f"Reached {i}/{len(self.chunck)} at {(i/len(self.chunck)) * 100}%")
        logging.info(f"Thread {self.name} finished and added to deletion list {len(deletion_list)} files")
        logging.info(f"Thread {self.name} finished with {len(self.chunck)} images to compare")
        self.ouput_list = deletion_list

    


def hash_image_thread(list, t_name, ts):
    logging.info(f"Thread {t_name} started with {len(list)} images to compare")
    deletion_list = []
    for p1, p2 in list:
        if hash_image_on_ts(p1,p2,ts):
            deletion_list.append((p1,p2))
    logging.info(f"Thread {t_name} finished with {len(list)} images to compare")
    return deletion_list

def find_duplicates_semantic_threaded(duplicates: list, ts, csv = None):
    number_of_cores = os.cpu_count()
    logging.info(f"Starting semantic evaluation on {number_of_cores} threads")
    splitted_list = list(split(duplicates, number_of_cores))
    threads = []
    for x in range(number_of_cores):
        threads.append(img_hash_thread(x, splitted_list[x], ts))
        
    for t in threads:
        t.start()
    # thanks to GIL this should make any difference to sequential version
    for t in threads:
        t.join()
    
    deletion_list = []
    for t in threads:
        deletion_list.extend(t.ouput_list)
    
    if csv:
        write_tuple_list_to_csv(path=csv, list = deletion_list)

    logging.info(f"Finished multithreaded image hashing, found {len(deletion_list)} elements for deletion")
    return [x[1] for x in deletion_list]


#splits a into n chunks
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))



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
    possible_duplicates = find_duplicates_by_name(path1_list, path2_list, lvl)
    # semantic dupcliate checking
    # with or without threading
    if t:
        deletion_list = find_duplicates_semantic_threaded(possible_duplicates, ts=ts, csv = csv)

    else:
        deletion_list = find_duplicates_semantic(possible_duplicates, ts=ts, csv = csv)
    if delete:
        if t:
            os_functions.del_list_threaded(deletion_list)
        else:
            os_functions.del_list(deletion_list)
    return