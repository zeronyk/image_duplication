```usage: main.py [-h] [-l LOG_FILE] [-o OUTPUT_CSV] [-d] [-t] [-ts IMAGEHASH_THRESHOLD] [-rem] [-lvl DIRECTORY_LEVEL] path1 [path1 ...] path2 [path2 ...]

Compare path2 to path1 and find all image duplicates listed in path1 and path2.

positional arguments:
  path1                 original path or list of paths
  path2                 path to check and optinal delete duplicates in

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_FILE, --log-file LOG_FILE
                        path of the log file to be written, defaults to duplicates.log in current folder
  -o OUTPUT_CSV, --output-csv OUTPUT_CSV
                        ouputs csv list of duplicates
  -d, --delete          automatically deletes duplicates
  -t, --threading       use multithreading to help speedup the process
  -ts IMAGEHASH_THRESHOLD, --imagehash-threshold IMAGEHASH_THRESHOLD
                        if not used -a how much simularity must be on the imagehash of the pictues (values will be interpreted as percent) default is 100
  -rem, --remove-other  removes other files, that are not considerd documents (good if there is a lot of junk) only works with -d
  -lvl DIRECTORY_LEVEL, --directory-level DIRECTORY_LEVEL
                        level of depth in namematching to be used while syntax finding duplicates (lvl= 0: consider every file, lvl=1: consider onlye files with same name, lvl=2: consider only
                        files with same named subfolder and same filename), default is 1