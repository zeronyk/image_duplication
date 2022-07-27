import pytest
import os 
import shutil
from image_duplicate_finder import find_duplicates

# aspects to test 
# delete x
# output_csv 
# threading x 
# imagehash-threashold x
# remove-other x
# directory level (not implemented)


# setting up all testfiles here 
path1 = os.path.join("/home/hermel/Documents/raid_utils/image_duplicate_finder/test/test_files", "path1")
path1_docs = os.path.join(path1, "fo1")
path1_trash = os.path.join(path1, "fo2")

path2 = os.path.join("/home/hermel/Documents/raid_utils/image_duplicate_finder/test/test_files", "path2")
path2_trash = os.path.join(path2, "fo21")
# other subfolder name
path2_docs = os.path.join(path2, "fo22")


trash_endings = (".cpp", ".log", ".re", ".we", ".m")
doc_endings = (".pdf", ".doc", ".docx")


picture_files = []
for root, dirs, files in os.walk("test_files/org_files/pictures", topdown=False):
    for file in files:
        if file.lower().endswith(".png"):
            picture_files.append(os.path.join("test_files/org_files/pictures", file))

picture_file_names = [os.path.basename(x) for x in picture_files]

trash_files = []
for root, dirs, files in os.walk("test_files/org_files/trash", topdown=False):
    for file in files:
        trash_files.append(os.path.join("test_files/org_files/trash", file))

trash_file_names = [os.path.basename(x) for x in trash_files]

document_files = []
for root, dirs, files in os.walk("test_files/org_files/documents", topdown=False):
    for file in files:
        document_files.append(os.path.join("test_files/org_files/documents", file))

document_file_names = [os.path.basename(x) for x in document_files]

def get_files(path):
    assert os.path.isdir(path)
    output = []
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            output.append(file)
    return output


def copy_into_folder(files, folder):
    for file in files:
        shutil.copyfile(file, os.path.join(folder, os.path.basename(file))) 

def del_tree(path): 
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

@pytest.fixture(scope="function", autouse=True)
def set_up_testfiles():
    assert os.path.exists("test_files")
    assert os.path.isdir("test_files")
    assert os.path.exists("test_files/org_files/trash")
    assert os.path.isdir("test_files/org_files/trash")
    assert os.path.exists("test_files/org_files/documents")
    assert os.path.isdir("test_files/org_files/documents")
    assert os.path.exists("test_files/org_files/pictures")
    assert os.path.isdir("test_files/org_files/pictures")
    

    os.mkdir(path1)
    os.mkdir(path1_docs)
    os.mkdir(path1_trash)
    os.mkdir(path2)
    os.mkdir(path2_trash)
    os.mkdir(path2_docs)

    copy_into_folder(picture_files, path1)
    copy_into_folder(picture_files, path1_docs)
    copy_into_folder(picture_files, path1_trash)
    copy_into_folder(picture_files, path2)
    copy_into_folder(picture_files, path2_trash)
    copy_into_folder(picture_files, path2_docs)


    copy_into_folder(document_files, path1_docs)
    copy_into_folder(trash_files, path1_trash)
    copy_into_folder(trash_files, path2_trash)
    copy_into_folder(document_files, path2_docs)
    
    

    yield

    del_tree(path1)
    del_tree(path2)

#@pytest.mark.parametrize("inputpath", [examplepath1, examplepath2, examplepath3, examplepath4, examplepath5, examplepath6])
def test_nothing():
    find_duplicates([path1], [path2], csv = None, delete = False, t = False, ts = 100, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)
    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)


    for x in picture_file_names:
        assert x in p1d
    
    for x in picture_file_names:
        assert x in p1t

    for x in picture_file_names:
        assert x in p1

    for x in picture_file_names:
        assert x in p2t

    for x in picture_file_names:
        assert x in p2d

    for x in picture_file_names:
        assert x in p2

    # check trash 
    for x in trash_file_names:
        assert not x in p1d
    
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert not x in p1

    for x in trash_file_names:
        assert x in p2t

    for x in trash_file_names:
        assert not x in p2d

    for x in trash_file_names:
        assert not x in p2


    # check documents
    for x in document_file_names:
        assert x in p1d
    
    for x in document_file_names:
        assert not x in p1t

    for x in document_file_names:
        assert not x in p1

    for x in document_file_names:
        assert not x in p2t

    for x in document_file_names:
        assert x in p2d

    for x in document_file_names:
        assert not x in p2

def test_deletion():
    find_duplicates([path1], [path2], csv = None, delete = True, t = False, ts = 100, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d

def test_deletion_remove_others():
    find_duplicates([path1], [path2], csv = None, delete = True, t = False, ts = 100, lvl = 1, remove_others = True)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert not x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert not x in p1t

    for x in trash_file_names:
        assert not x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d
    
def test_nothing_threaded():
    find_duplicates([path1], [path2], csv = None, delete = False, t = True, ts = 100, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)
    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)


    for x in picture_file_names:
        assert x in p1d
    
    for x in picture_file_names:
        assert x in p1t

    for x in picture_file_names:
        assert x in p1

    for x in picture_file_names:
        assert x in p2t

    for x in picture_file_names:
        assert x in p2d

    for x in picture_file_names:
        assert x in p2

    # check trash 
    for x in trash_file_names:
        assert not x in p1d
    
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert not x in p1

    for x in trash_file_names:
        assert x in p2t

    for x in trash_file_names:
        assert not x in p2d

    for x in trash_file_names:
        assert not x in p2


    # check documents
    for x in document_file_names:
        assert x in p1d
    
    for x in document_file_names:
        assert not x in p1t

    for x in document_file_names:
        assert not x in p1

    for x in document_file_names:
        assert not x in p2t

    for x in document_file_names:
        assert x in p2d

    for x in document_file_names:
        assert not x in p2

def test_deletion_threaded():
    find_duplicates([path1], [path2], csv = None, delete = True, t = True, ts = 100, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d

def test_deletion_remove_others_threaded():
    find_duplicates([path1], [path2], csv = None, delete = True, t = True, ts = 60, lvl = 1, remove_others = True)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert not x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert not x in p1t

    for x in trash_file_names:
        assert not x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d
# this is not a good test but i dont have any pictures having ts i9
def test_deletion_ts():
    find_duplicates([path1], [path2], csv = None, delete = True, t = False, ts = 60, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d

def test_deletion_csv():
    find_duplicates([path1], [path2], csv = os.path.join(os.path.abspath(os.getcwd()), "test.csv"), delete = True, t = False, ts = 60, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d


    assert os.path.exists(os.path.join(os.path.abspath(os.getcwd()), "test.csv"))
    with open(os.path.join(os.path.abspath(os.getcwd()), "test.csv"), "r") as f:
        assert len(f.readlines()) > 0

    os.remove(os.path.join(os.path.abspath(os.getcwd()), "test.csv")) 


def test_deletion_csv_threaded():
    find_duplicates([path1], [path2], csv = os.path.join(os.path.abspath(os.getcwd()), "test.csv"), delete = True, t = True, ts = 60, lvl = 1, remove_others = False)
    # check pictures 

    p1d = os.listdir(path1_docs)
    p1t = os.listdir(path1_trash)
    p1 = os.listdir(path1)

    p2t = os.listdir(path2_trash)
    p2d = os.listdir(path2_docs)
    p2 = os.listdir(path2)

    file_list = []
    file_list.extend(p1d)
    file_list.extend(p1t)
    file_list.extend(p1)
    file_list.extend(p2t)
    file_list.extend(p2d)
    file_list.extend(p2)

    unique_picture = set()

    
    for x in file_list:
        if x.endswith(".png"):
            assert x not in unique_picture
            unique_picture.add(x)

    for x in picture_file_names:
        assert x in unique_picture

    # check trash
    unique_trash = set()
    for x in file_list:
        if x.endswith(trash_endings):
            unique_trash.add(x)

    for x in trash_file_names:
        assert x in unique_trash
    # check trash folder sperate
    for x in trash_file_names:
        assert x in p1t

    for x in trash_file_names:
        assert x in p2t


    # check docs
    unique_docs = set()
    for x in file_list:
        if x.endswith(doc_endings):
            unique_docs.add(x)

    for x in document_file_names:
        assert x in unique_docs

    # check docs folder sperate
    for x in document_file_names:
        assert x in p1d

    for x in document_file_names:
        assert x in p2d

    assert os.path.exists(os.path.join(os.path.abspath(os.getcwd()), "test.csv"))
    with open(os.path.join(os.path.abspath(os.getcwd()), "test.csv"), "r") as f:
        assert len(f.readlines()) > 0

    os.remove(os.path.join(os.path.abspath(os.getcwd()), "test.csv")) 