'''
################################################################################
GET FILES FROM DATA DIRECTORIES
################################################################################
'''
def get_nii_files(main_directory,dir_list, file_list, text,extension):
    import os

    folder_file={}
    for ii in dir_list:
        #print(ii)
        fulldir = os.path.join(main_directory,ii)
        for jj in file_list[ii]:
            if text in jj: #found a matching file
                #print(jj)
                if extension in jj:
                    folder_file[ii] = jj
                    print('found proper ',text, jj)


    print(folder_file)
    return folder_file
