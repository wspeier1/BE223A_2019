'''
GET FILE LISTING----------------------------------------------------------------
'''
def get_dirs(top_dir = "/home/kgonzalez/BIOENG223A_FALL_2019/data/"):
    import os

    print('Running get_dirs: ',top_dir)
    
    dir_list = os.scandir(top_dir)
    directories=[]
    file_list = {}
    for ii in dir_list:
        file_list[ii.name]=[]
        directories.append(ii.name)
        #get file listings for each directory found
        files = os.scandir(os.path.join(top_dir,ii.name))
        for jj in files:
            file_list[ii.name].append(jj.name)


    
    return directories, file_list


