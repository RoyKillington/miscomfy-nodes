import os
import torch
import aiohttp
import asyncio
import numpy as np
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

class VeniceUpscale:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('VENICE_API_KEY')
        self.base_url = os.getenv('BASE_URL')

    @classmethod
    def INPUT_TYPES(cls):
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

    FUNCTION = "main_sync"

    #OUTPUT_NODE = False

    CATEGORY = "image/upscaling"

    # Take a tensor from Comfy and make it byte
    def tensor_to_bytes(self, image_tensor):
        print(f"Converting tensor to bytes for image shape: {image_tensor.shape}")
        image_tensor = image_tensor.squeeze(0)
        numpy_image = image_tensor.cpu().numpy()
        if numpy_image.dtype == np.float32:
            numpy_image = (numpy_image * 255).astype(np.uint8)
        pil_image = Image.fromarray(numpy_image, 'RGB')

        with BytesIO() as buffer:
            pil_image.save(buffer, format='PNG')

            return buffer.getvalue()

    # Take an image from the input & make it a tensor to keep interacting with
    def bytes_to_tensor(self, image_bytes):
        print(f"Converting bytes to tensor for image bytes size: {len(image_bytes)}")
        pil_image = Image.open(BytesIO(image_bytes))    # Decode the image
        np_image = np.array(pil_image)                  # Make it an array....

        # Check the shape and mode of the image
        print(f"PIL image mode: {pil_image.mode}, shape: {np_image.shape}")

        # Convert to RGB if necessary
        if pil_image.mode == 'RGBA':  # If the image has an alpha channel, convert to RGB
            np_image = np_image[:, :, :3]
        elif pil_image.mode == 'L':   # Grayscale image
            np_image = np.stack((np_image,) * 3, axis=-1)  # Convert grayscale to RGB

        # Ensure the image is in RGB format
        if len(np_image.shape) == 2:  # Grayscale image
            np_image = np.stack((np_image,) * 3, axis=-1)  # Convert grayscale to RGB

        image_tensor = torch.from_numpy(np_image)       # Turn that into a tensor [H,W,C]
        image_tensor = image_tensor.to(torch.float32)   # Explicity cast is as 32-bit
        image_tensor = image_tensor / 255.0             # Normalize it
        image_tensor = image_tensor.unsqueeze(0)

        return image_tensor

    async def async_upscale(self, url, payload, headers, image_bytes):
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('image', image_bytes, filename='image.png', content_type='image/png')
            form_data.add_field('scale', payload['scale'])

            async with session.post(url, headers=headers, data=form_data) as response:
                if response.status != 200:
                    raise Exception(f"API request failed with status {response.status}: {await response.text()}")
                print(f"Received response with status {response.status}")
                return await response.read()

    async def main(self, image, scale):
        images = image
        images_list = []
        upscaled_tensors = []

        # Set up the non-image API stuff
        api_key = self.api_key
        base_url = self.base_url
        url = f'{base_url}/image/upscale'
        headers = {"Authorization": f'Bearer {api_key}'}
        scale = str(scale)
        payload = {'scale': scale}

        # Convert each image in the tensor into a PNG
        batch_size = images.size(0)
        print(f"Batch size: {batch_size}")
        for i in range(batch_size):
            image = images[i]
            image_bytes = self.tensor_to_bytes(image)
            images_list.append(image_bytes)
        print(f"Converted {len(images_list)} images to bytes")

        # Create a list of tasks for each PNG in the list
        tasks = []
        for image_bytes in images_list:
            task = self.async_upscale(url, payload, headers, image_bytes)
            tasks.append(task)
        print(f"Created {len(tasks)} tasks for asynchronous processing")

        # Run all the tasks concurrently and collect the results
        upscaled_bytes_list = await asyncio.gather(*tasks)
        print(f"Received {len(upscaled_bytes_list)} upscaled images")

        # Convert each upscaled byte response into a tensor
        for upscaled_bytes in upscaled_bytes_list:
            upscaled_tensor = self.bytes_to_tensor(upscaled_bytes)
            print(f"Upscaled tensor shape: {upscaled_tensor.shape}, dtype: {upscaled_tensor.dtype}")
            upscaled_tensors.append(upscaled_tensor)
        print(f"Converted {len(upscaled_tensors)} bytes to tensors")

        concat_tensor = torch.cat(upscaled_tensors)
        print(f"Concatenated tensor shape: {concat_tensor.shape}")
        return (concat_tensor,) # Output the upscaled tensor from the node

    def main_sync(self, image, scale):
        return asyncio.run(self.main(image, scale))

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "VeniceUpscale": VeniceUpscale
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "VeniceUpscale": "Venice AI Upscale"
}
