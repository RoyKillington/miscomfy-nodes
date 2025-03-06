# Miscomfy Nodes

A repo of custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) nodes made by me to do many different things.
## Installation
1. **ComfyManager**: this node repo is not currently listed in the the ComfyManager registry. Manual installation is required at this time and is compatble with use of ComfyManager
2. **Manual**: clone or download the repo.  move out copy it into the *custom_nodes* directory of your Comfyui install. Restart the server if it's running.

## Nodes Included
- **Venice AI Upscaler**: takes, transforms, and sends your decoded VAE outputs to [Venice.AI's](https://venice.ai) [image upscaler](https://docs.venice.ai/api-reference/endpoint/image/upscale) before turning the response back into tensors for further manipulation. Can take batches of tensors and outputs the same. No rate limit safeguards implemented yet.

## Nodes Planned
- **Venice AI Image Generator**: allows image generation using [Venice.AI's](https://venice.ai) [image generation models](https://docs.venice.ai/api-reference/endpoint/image/generate).
- **Venice AI Text Prompt Generator**: allows text generation using [Venice.AI's](https://venice.ai) [text generation models](https://docs.venice.ai/api-reference/endpoint/chat/completions) for whatever needs you have
- **Venice AI Quality Assuarance**: uses a vision model at [Venice.AI's](https://venice.ai) [text generation models](https://docs.venice.ai/api-reference/endpoint/chat/completions) to look at your generations and help you cull the really bad ones (might not work)

### TODO
1. ~~Add batch>1 to *Venice AI Upscaler*~~
2. Add installation instructions sans ComfyManager
3. Add use instructions for *Venice AI Upscaler*
4. Basic textgen prompt node (Danbooru syatem prompt?)
5. VUpscale: Protect against hitting rate limits

## Contributing
At the moment, not looking for extra contributors, but fork and send a push request if you are interested/have a suggestion
