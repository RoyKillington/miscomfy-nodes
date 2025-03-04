# Miscomfy Nodes

A repo of custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) nodes made by me to do many different things.
## Nodes Included
- **Venice AI Upscaler**: takes, transforms, and sends your decoded VAE outputs to [Venice.AI's](https://venice.ai) [image upscaler](https://docs.venice.ai/api-reference/endpoint/image/upscale) before turning the response back into tensor for further manipulation. Currently only can take *batch 1* or else it throws an error

## Nodes Planned
- **Venice AI Image Generator**: allows image generation using [Venice.AI's](https://venice.ai) [image generation models](https://docs.venice.ai/api-reference/endpoint/image/generate).
- **Venice AI Text Prompt Generator**: allows text generation using [Venice.AI's](https://venice.ai) [text generation models](https://docs.venice.ai/api-reference/endpoint/chat/completions) for whatever needs you have
- **Venice AI Quality Assuarance**: uses a vision model at [Venice.AI's](https://venice.ai) [text generation models](https://docs.venice.ai/api-reference/endpoint/chat/completions) to look at your generations and help you cull the really bad ones

### TODO
1. Add batch>1 to *Venice AI Upscaler*
2. Start work on next node
3. Add installation instructions sans ComfyManager
4. Add use instructions for *Venice AI Upscaler*

## Contributing
At the moment, not looking for extra contributors, but fork and send a push request if you are interested/have a suggestion
