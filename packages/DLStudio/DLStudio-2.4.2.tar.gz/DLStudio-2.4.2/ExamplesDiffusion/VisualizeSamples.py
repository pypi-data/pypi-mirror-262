
##  VisualizeSamples.py

##  See the README in the ExamplesDiffusion directory for how to use this script for
##  extracting the images from the numpy archive created by the script
##  GenerateNewImageSamples.py


import numpy as np
import matplotlib.pyplot as plt

data = np.load("RESULTS/samples_8x64x64x3.npz")

print("\n\n[visualize_sample.py]  the data object: ", data)                                       ## NpzFile 'RESULTS/samples_8x64x64x3.npz' with keys: arr_0
print("\n\n[visualize_sample.py]  type of the data object: ", type(data))                         ## <class 'numpy.lib.npyio.NpzFile'>
print("\n\n[visualize_sample.py]  shape of the object data['arr_0']: ", data['arr_0'].shape)      ## (8, 64, 64, 3)

for i, img in enumerate(data['arr_0']):
    plt.figure()
    plt.imshow(img)
    plt.axis("off")
    plt.savefig(f"visualize_samples/test_{i}.jpeg")
    
