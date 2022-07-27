# ImageDuplicationFinder
Finds duplicated images in Folders. It finds duplicated images first matched on the name. So **both images have to have the same name**. After a match is found based on the name, it will compare image hashes to make sure the both images are identical!

-------

Usecase: You have multiple hard-drives, which all contain pictures. But are messy copied (for example after recovery). Copy both hard drives on a single one, or remove every duplicated picture from your hard-drives.


## Installation
-----
> pip install ImageDuplicationFinder 

or just clone this repository and run 

>pip install .

## Overview
-----
 - There are 3 stages : 
 
  - 0:Syntax match (find identical names), 
  - 1:Semantic match (compare images based on the pixelvalue)
  - 2:Deletion (delete Syntax AND Semantic matches)

 - If you only want to check for duplication, use -csv flag, it will print out a csv file with found dupications at the destination path given (skipping deletion stage)

 - This programm will remove all duplicates from path1 AND path2! If you have duplications in the path1 folder, they will be found!
 
 - This program is designed for big workloads (> 1tb ) in mind, it supports multithreading for speedup (will spawn as many threads as cores) and log the process to 

 - This program will output a log file on the log position, will create a logfile at default (duplication.log)

 - deletion is made at the very end, so if you break in comparison-stage, you wont delete anything


## Features in progress
---- 
- make Syntax matching optional (use lvl parameter)
- copy all data to a destination folder after duplication removal


## Formates 
----- 
Images and junk are destinct by formates, (only matters if run with the remove-other option) :

- **Not junk**: ('.wav', '.mp3', '.png', '.jpg', '.jpeg', '.gif', '.tiff', '.psd','.bmp', '.eps', '.ai', '.indd', '.raw', '.webm', '.mkv', '.flv', '.vob', '.ogv', '.ogg', '.drc', '.gif', '.mng', '.avi', '.mts', '.m2ts', '.ts', '.mov', '.qt', '.wmv', '.yuv', '.rm', '.rmvb', '.viv', '.asf', '.mp4', '.m4p', '.m4v', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mpg', '.mpeg', '.m2v', '.m4v', '.svi','.3gp', '.3g2', '.mxf', '.roq', '.nsv', '.flv', '.f4v', '.f4p','.f4a', '.f4b', '.doc', '.pdf', '.docx', '.docm', '.dot', '.odt', '.rtf', '.txt', '.csv', '.dif', '.xls')

- **Images**: (".png", ".jpg", ".jpeg", '.gif')


## Usage
-------

> idf -h

```
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
```
or use as python function 

```
from image_duplicate_finder import find_duplicates


find_duplicates(path1, path2, csv = None, delete = False, t = False, ts = 100, lvl = 1, remove_others = False)

```