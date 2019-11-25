'''
ANIMATE IMAGES------------------------------------------------------------------
'''
def animate_image(image_dir, base_filename, stack):
    plt.close()
    plt.rcParams["animation.html"] = "jshtml"

    #plt.figure()
    #plt.imshow(stack[:,:,300])
    fig=plt.figure()
    #plt.imshow(stack[:,:,255])
    ims = []
    dir_name = image_dir #"/home/kgonzalez/IMAGES"
    #base_filename = "figure"
    filename_suffix = ".png"
    x,y,num_frames = np.shape(stack) 
    print('number of frames to animate is ',num_frames)
    for ii in range(0,num_frames):
        im = plt.imshow(stack[:,:,ii], animated=True)
        ims.append([im])
        plt.imshow(stack[:,:,ii],cmap='gray')
        plt.title('CT Skull Image')
        name = os.path.join(dir_name, base_filename + str(ii).zfill(5)  + filename_suffix)
        #print('name is: ',name)
        
        plt.savefig(name) # save as png
    print('done animating images')
    plt.show()
    ani = animation.ArtistAnimation(fig, ims, interval=1000, blit=True,
        repeat_delay=500)
    #plt.show()
    mp4name = os.path.join(dir_name, 'dyn.mp4')
    ani.save(mp4name)
    print('done with animation mp4')
    return 0

