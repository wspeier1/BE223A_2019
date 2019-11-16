
'''
APPLY MARKERS TO POINTS DETERMINED TO BE METAL
'''

def apply_marker_to_metal(mloc_dict,
                        stacked,
                        second_marker=0,
                        cmapin='bone',
                        marker_color='r',
                        second_dict = {},
                        second_marker_color = 'g',
                        write_to_disk =0,
                        output_folder =''):

    import matplotlib.pyplot as plt
    import os    
    
    if (write_to_disk == 1):
        if not os.path.exists(output_folder):
            print('path does not exist. trying to make')
            os.mkdir(output_folder)
    
    
    '''
    Take in data and put markers over dictionary areas indicating metal was found
    '''
    
    print('Plotting sequence with metal points: #points= ',len(mloc_dict))

    for current_slice_key in mloc_dict:
        #if (len(current_slice_key) == 0):
        #    #found an empty list
        #    continue
        print('current slice is',current_slice_key)
        fig,ax = plt.subplots()
        plt.imshow(stacked[:,:,current_slice_key],cmap=cmapin)

        for entry in mloc_dict[current_slice_key]:
            row = entry[0]
            col = entry[1]

            circle1 = plt.Circle((col,row), 1,color=marker_color, fill=False)
            ax.add_patch(circle1)

        if ((second_marker == 1) and (current_slice_key in second_dict)):
            for entry2 in second_dict[current_slice_key]:
                row2 = entry2[0]
                col2 = entry2[1]

                circle2 = plt.Circle((col2,row2), 1,color=second_marker_color, fill=False)
                ax.add_patch(circle2)




        plt.colorbar()
        title_text = 'Image Slice #' + str(current_slice_key)
        plt.title(title_text) #current_slice_key)
        #plt.show()
        
        #
        # Write sample images to a folder for review
        #
        if (write_to_disk == 1):
            extension = '.png'
            #output_folder = '/content/gdrive/My Drive/PAPER_DATA'
            figname = 'Figure_' + str(current_slice_key) + extension
            out_name = os.path.join(output_folder, figname)
            fig.savefig(out_name,dpi=300, bbox_inches='tight')
            #make sure to save under fig, since it was opened with a handle
            #plt.close()

        plt.show()




    return 0
