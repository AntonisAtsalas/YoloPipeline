import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Decolorization function
def decolorize(img_fname, scale=None, effect=.5, noise=.001):
    # Read image as matrix.
    RGB = mpimg.imread(img_fname)
    
    # We need the values to be on [0, 1].
    if RGB.dtype != 'float32':
        if (np.min(RGB) >= 0) and (np.max(RGB) <= 255):
            RGB = RGB.astype(float) / 255
    
    dims = np.shape(RGB)
    
    # If the image is black and white, we only have 
    # the luminance channel itself (Y/L).
    if len(dims) == 1: 
        print('Image is already decolorized.')
        return RGB
    
    tol = 100*np.finfo(float).eps
    if scale is None: scale = np.sqrt(2*min(dims[0:2]))

    # Remove transparency channel, if any.
    if dims[2] == 4: 
        RGB = RGB[:,:,0:3]
        dims = np.shape(RGB)
    
    # Compute achromatic luminance (Y) and the orthogonal chromatic channels (P, Q).
    RGB = RGB.transpose(2,1,0).reshape(dims[2],dims[0]*dims[1])
    Weights = np.array([[0.2989360212937753847527155, 0.5870430744511212909351327, 0.1140209042551033243121518],
                        [.5000, .5000, -1.00],
                        [1.000, -1.00, 0.000]])
    YPQ = Weights.dot(RGB)
    [Y,P,Q] = map(np.squeeze, np.split(YPQ, 3, axis=0))

    # Modify lumimence channel (L) and compute saturation (S)
    Lmax = 1
    Lscale = 0.66856793424088827189
    Smax = 1.1180339887498948482 
    alter = effect*(Lmax/Smax)

    # Compute chroma channel (Ch)
    Ch = np.sqrt(np.square(P) + np.square(Q))

    # Sample each pixel's neighborhood.
    mesh = np.meshgrid(range(dims[0]), range(dims[1]))
    mesh = np.dstack([mesh[0], mesh[1]]).reshape(-1, 2)
    displace = scale * np.sqrt(2/np.pi) * np.random.normal(size=[dims[0]*dims[1],2])
    look = np.round(mesh + displace)
    redo = look[:,0] < 0
    look[redo,0] = (abs(look[redo,0]) % dims[0])
    redo = look[:,1] < 0
    look[redo,1] = (abs(look[redo,1]) % dims[1])    
    redo = look[:,0] >= dims[0]
    look[redo,0] = dims[0] - (look[redo,0] % dims[0]) -1
    redo = look[:,1] >= dims[1]
    look[redo,1] = dims[1] - (look[redo,1] % dims[1]) -1
    look = (look[:,0] + dims[0] * look[:,1]).astype(int)
    
    # Compute
    delta = YPQ - YPQ[:,look]
    contrast_change = abs(delta[0,:])
    contrast_dir = np.sign(delta[0,:])
    color_diff = RGB.astype('float') - RGB[:,look].astype('float')
    color_diff = np.sqrt(sum(np.square(color_diff), 1)) + np.finfo(float).eps

    w = 1 - np.divide(contrast_change/Lscale, color_diff)
    w[color_diff < tol] = 0
    axis = np.multiply(w, contrast_dir)
    axis = np.multiply(delta[1:3,:], np.array([axis, axis]))
    axis = np.sum(axis,1)
    
    proj = YPQ[1,:]*axis[0] + YPQ[2,:]*axis[1]
    proj = proj / (np.quantile(abs(proj), 1-noise) + tol)
    
    # L: luminance channel (black-and-white image)
    # C: color projection channel
    L = YPQ[0,:]
    C = effect*proj
    
    # G: composite, decolorized image
    G = L + C 
    img_range = np.quantile(G, (noise, 1-noise))
    G = (G - img_range[0]) / (img_range[1] - img_range[0] + tol)
    tgt_range = effect * np.array([0, Lmax]) + (1-effect) * np.quantile(YPQ[0,:], (noise, 1-noise))
    G = tgt_range[0] + G*(tgt_range[1] - tgt_range[0] + tol)
    G = np.minimum(np.maximum(G, YPQ[0,:] - alter*Ch), YPQ[0,:] + alter*Ch)
    G = np.minimum(np.maximum(G, 0), Lmax)
    
    (G, L, C) = [X.reshape(dims[1], dims[0]).transpose() for X in (G, L, C)]
    
    GLC = np.stack([G, L,C]).transpose([1,2,0])
    
    return GLC

# Directory paths
input_dir = 'C:\\Users\\user\\Documents\\elies\\initial data\\new'
output_dir = 'C:\\Users\\user\\Documents\\elies\\initial data\\decolorize'

# Iterate over files in the input directory
for filename in os.listdir(input_dir):
    if filename.startswith("r_") and filename.endswith(".png"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Perform decolorization
        decolorized_image = decolorize(input_path)
        
        # Save the decolorized image
        plt.imsave(output_path, decolorized_image[:,:,0], cmap=plt.cm.gray, vmin=0, vmax=1)

print("Decolorization complete.")
