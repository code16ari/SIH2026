import numpy as np
import torch

print("================================")
print("     GIS -> ML CONNECTION TEST")
print("================================")

# Simulated satellite image
# 4 bands, 256 x 256 pixels
satellite_image = np.random.rand(4, 256, 256).astype(np.float32)

print("NumPy image shape:", satellite_image.shape)

# NumPy -> PyTorch
tensor = torch.from_numpy(satellite_image)

print("PyTorch tensor shape:", tensor.shape)
print("Tensor type:", tensor.dtype)

# Add batch dimension
tensor = tensor.unsqueeze(0)

print("ML input shape:", tensor.shape)

print("================================")
print("GIS -> ML CONNECTION WORKING!")
print("================================")