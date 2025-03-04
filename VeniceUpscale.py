import os
import requests
import torch
import numpy as np
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

class VeniceUpscale:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('VENICE_API_KEY')
        self.base_url = os.getenv('BASE_URL')
        self.original_input_was_normalized = None
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "scale": ("INT", {
                    "default": 4,
                    "min": 2,
                    "max": 4,
                    "step": 2,
                    "display": "slider"
                })
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ()

    FUNCTION = "upscale"

    #OUTPUT_NODE = False

    CATEGORY = "image/upscaling"

    # Take a tensor from Comfy and make it byte
    def tensor_to_bytes(self, image_tensor):
        ### TODO__ Manage actual batch stuff. Right now, it just crashes the node to have a batch size greater than 1
        image_tensor = image_tensor.squeeze(0)
        
        numpy_image = image_tensor.cpu().numpy()
        
        # Handle float -> uint8 conversion
        if numpy_image.dtype == np.float32:
            numpy_image = (numpy_image * 255).astype(np.uint8)
        
        # Direct conversion without dimension shuffling
        pil_image = Image.fromarray(numpy_image, 'RGB')
        
        with BytesIO() as buffer:
            pil_image.save(buffer, format='PNG')
            
            return buffer.getvalue()

    # Take an image from the input & make it a tensor to keep interacting with
    def bytes_to_tensor(self, image_bytes):             
        pil_image = Image.open(BytesIO(image_bytes))    # Decode the image    
        np_image = np.array(pil_image)                  # Make it an array....

        image_tensor = torch.from_numpy(np_image)       # Turn that into a tensor [H,W,C]
        image_tensor = image_tensor.unsqueeze(0)        # Add the Batch again [B,H,W,C]
        image_tensor = image_tensor.to(torch.float32)   # Explicity cast is as 32-bit
        image_tensor = image_tensor / 255.0             # Normalize it

        return image_tensor
        
    def upscale(self, image, scale):                # Main method of the node
        image_bytes = self.tensor_to_bytes(image)   # Turn the tensor input into a PNG for the API

        api_key = self.api_key                      # Set up the logistical stuff with the API
        base_url = self.base_url
        url = f'{base_url}/image/upscale'

        scale = str(scale)                          # Set up the actual information for the API
        payload = {'scale': scale}
        files = {'image': ('image.png', image_bytes, 'image/png')}
        headers = {"Authorization": f'Bearer {api_key}'}
        
        # Post the PNG to the API & throw an error if necessay
        response = requests.request("POST", url, data=payload, files=files, headers=headers)
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        upscaled_tensor = self.bytes_to_tensor(response.content) # Take the upscaled PNG and make it a tensor again for Comfy

        return (upscaled_tensor,) # Output the upscaled tensor from the node

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "VeniceUpscale": VeniceUpscale
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VeniceUpscale": "Venice AI Upscale"
}
