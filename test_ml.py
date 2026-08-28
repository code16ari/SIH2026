import torch
import torchvision

print("================================")
print("      ML ENVIRONMENT TEST")
print("================================")

print("PyTorch version :", torch.__version__)
print("Torchvision     :", torchvision.__version__)

print("CUDA available  :", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU             :", torch.cuda.get_device_name(0))
else:
    print("GPU             : Not available")

print("================================")
print("ML ENVIRONMENT WORKING!")
print("================================")