'''
Celluloid animation package
'''
def cell_animate(image_dir, 
                 base_filename, 
                 stack,
                 slice_column =2,
                 cmapin='bone',
                 cbar = 1):
    fig = plt.figure()
    camera = Camera(fig)

    #fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize=(5, 5),squeeze=False)
    #camera = Camera(fig)

    dir_name = image_dir #"/home/kgonzalez/IMAGES"
    #base_filename = "figure"
    filename_suffix = ".png"
    x,y,num_frames = np.shape(stack) 

    vidfile = os.path.join(dir_name,'animatedct.gif');
    for ii in range(0,num_frames):
        
        plt.imshow(stack[:,:,ii],cmap=cmapin)
        plt.title('CT Skull Image')
        #if (cbar == 1):
        #    plt.colorbar()
        #im0 = axes[0].imshow(stack[:,:,ii],cmap=cmapin);
        #use fraction and pad to shrink colorbar to fit image
        #fig.colorbar(im0, ax=axes[0],fraction=0.046, pad=0.04)
        #name = os.path.join(dir_name, base_filename + str(ii).zfill(5)  + filename_suffix)
        #print('name is: ',name)
        
        #plt.savefig(name) # save as png

        camera.snap()
    animation = camera.animate()
    animation.save(vidfile, writer = 'imagemagick')


    return 0
