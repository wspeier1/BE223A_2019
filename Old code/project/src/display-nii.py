import sys
import nibabel as nib
from mayavi import mlab
from mayavi.tools.mlab_scene_model import MlabSceneModel
from traits.api import HasTraits, Instance

class Visualization(HasTraits):
	scene = Instance(MlabSceneModel, ())

	def __init__(self, nib_file):
		image_data = nib.load(nib_file)
		self.plot = self.scene.mlab.contour3d(image_data.get_data(), color=(1.0, .4, 0.7))

def main():
	mlab.clf()
	for i in range(1, len(sys.argv)):
		image_data = nib.load(sys.argv[i])
		mlab.contour3d(image_data.get_data())
	mlab.show()

main()
