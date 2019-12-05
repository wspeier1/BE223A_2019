
'''
################################################################################
Load Hull file containing cortical surface boundaries
################################################################################
'''
def load_hull_file(f_hull):
    import nibabel as nib         #pull in library


    ### Load one of the files
    #f_hull = os.path.join(path_dict[4,0],file_dict[4,0])
    print('hull filename is ',f_hull)
    hull_img = nib.load(f_hull)
    hull_data = hull_img.get_fdata()

    return hull_data


