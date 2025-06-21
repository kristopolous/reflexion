2. [Home](/)
4. [Explore](/models)
6. fal-ai/flux-pro/kontext/max

[Docs](https://docs.fal.ai)[Blog](https://blog.fal.ai)[Pricing](/pricing)[Enterprise](/enterprise)[Careers](/careers)[Research Grants](/grants)

[Log-in](/login?returnTo=/models/fal-ai/flux-pro/kontext/max/api)[Sign-up](/login?returnTo=/models/fal-ai/flux-pro/kontext/max/api)

1. [Back to Gallery](/models)

# FLUX.1 Kontext [max] Image to Image

fal-ai/flux-pro/kontext/max

Kontext [max] -- Editing

FLUX.1 Kontext [max] is a model with greatly improved prompt adherence and typography generation meet premium consistency for editing without compromise on speed.

Inference

Commercial use

Partner

[Schema](/api/openapi/queue/openapi.json?endpoint_id=fal-ai/flux-pro/kontext/max)

[Playground](/models/fal-ai/flux-pro/kontext/max/playground)[API](/models/fal-ai/flux-pro/kontext/max/api)[Examples](/models/fal-ai/flux-pro/kontext/max/examples)

### Table of contents

JavaScript / Node.js

[#### 1. Calling the API](/models/fal-ai/flux-pro/kontext/max/api#api-call)

* [Install the client](/models/fal-ai/flux-pro/kontext/max/api#api-call-install)
* [Setup your API Key](/models/fal-ai/flux-pro/kontext/max/api#api-call-setup)
* [Submit a request](/models/fal-ai/flux-pro/kontext/max/api#api-call-submit-request)

[#### 2. Authentication](/models/fal-ai/flux-pro/kontext/max/api#auth)

* [API Key](/models/fal-ai/flux-pro/kontext/max/api#auth-api-key)

[#### 3. Queue](/models/fal-ai/flux-pro/kontext/max/api#queue)

* [Submit a request](/models/fal-ai/flux-pro/kontext/max/api#queue-submit)
* [Fetch request status](/models/fal-ai/flux-pro/kontext/max/api#queue-status)
* [Get the result](/models/fal-ai/flux-pro/kontext/max/api#queue-result)

[#### 4. Files](/models/fal-ai/flux-pro/kontext/max/api#files)

* [Data URI (base64)](/models/fal-ai/flux-pro/kontext/max/api#files-data-uri)
* [Hosted files (URL)](/models/fal-ai/flux-pro/kontext/max/api#files-from-url)
* [Uploading files](/models/fal-ai/flux-pro/kontext/max/api#files-upload)

[#### 5. Schema](/models/fal-ai/flux-pro/kontext/max/api#schema)

* [Input](/models/fal-ai/flux-pro/kontext/max/api#schema-input)
* [Output](/models/fal-ai/flux-pro/kontext/max/api#schema-output)
* [Other](/models/fal-ai/flux-pro/kontext/max/api#schema-other)

### About

FLUX.1 Kontext [Max] -- Frontier image editing model.

Kontext Max is a more powerful version of Kontext that can handle more complex tasks.

### 1. Calling the API[#](#api-call-install)

### Install the client[#](#api-call-install)

The client provides a convenient way to interact with the model API.

npmyarnpnpmbun

```
npm install --save @fal-ai/client
```

##### Migrate to @fal-ai/client

The `@fal-ai/serverless-client` package has been deprecated in favor of `@fal-ai/client`. Please check the [migration guide](https://docs.fal.ai/clients/javascript#migration-from-serverless-client-to-client) for more information.

### Setup your API Key[#](#api-call-setup)

Set `FAL_KEY` as an environment variable in your runtime.

```
export FAL_KEY="YOUR_API_KEY"
```

### Submit a request[#](#api-call-submit-request)

The client API handles the API submit protocol. It will handle the request status updates and return the result when the request is completed.

```
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext/max", {
  input: {
    prompt: "Put a donut next to the flour.",
    image_url: "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});
console.log(result.data);
console.log(result.requestId);
```

## 2. Authentication[#](#auth)

The API uses an API Key for authentication. It is recommended you set the `FAL_KEY` environment variable in your runtime when possible.

### API Key[#](#auth-api-key)

In case your app is running in an environment where you cannot set environment variables, you can set the API Key manually as a client configuration.

```
import { fal } from "@fal-ai/client";

fal.config({
  credentials: "YOUR_FAL_KEY"
});
```

##### Protect your API Key

When running code on the client-side (e.g. in a browser, mobile app or GUI applications), make sure to not expose your `FAL_KEY`. Instead, **use a server-side proxy** to make requests to the API. For more information, check out our [server-side integration guide](https://docs.fal.ai/model-endpoints/server-side).

## 3. Queue[#](#queue)

##### Long-running requests

For long-running requests, such as *training* jobs or models with slower inference times, it is recommended to check the [Queue](https://docs.fal.ai/model-endpoints/queue) status and rely on [Webhooks](https://docs.fal.ai/model-endpoints/webhooks) instead of blocking while waiting for the result.

### Submit a request[#](#queue-submit)

The client API provides a convenient way to submit requests to the model.

```
import { fal } from "@fal-ai/client";

const { request_id } = await fal.queue.submit("fal-ai/flux-pro/kontext/max", {
  input: {
    prompt: "Put a donut next to the flour.",
    image_url: "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
  },
  webhookUrl: "https://optional.webhook.url/for/results",
});
```

### Fetch request status[#](#queue-status)

You can fetch the status of a request to check if it is completed or still in progress.

```
import { fal } from "@fal-ai/client";

const status = await fal.queue.status("fal-ai/flux-pro/kontext/max", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b",
  logs: true,
});
```

### Get the result[#](#queue-result)

Once the request is completed, you can fetch the result. See the [Output Schema](#schema-output) for the expected result format.

```
import { fal } from "@fal-ai/client";

const result = await fal.queue.result("fal-ai/flux-pro/kontext/max", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b"
});
console.log(result.data);
console.log(result.requestId);
```

## 4. Files[#](#files)

Some attributes in the API accept file URLs as input. Whenever that's the case you can pass your own URL or a Base64 data URI.

### Data URI (base64)[#](#files-data-uri)

You can pass a Base64 data URI as a file input. The API will handle the file decoding for you. Keep in mind that for large files, this alternative although convenient can impact the request performance.

### Hosted files (URL)[#](#files-from-url)

You can also pass your own URLs as long as they are publicly accessible. Be aware that some hosts might block cross-site requests, rate-limit, or consider the request as a bot.

### Uploading files[#](#files-upload)

We provide a convenient file storage that allows you to upload files and use them in your requests. You can upload files using the client API and use the returned URL in your requests.

```
import { fal } from "@fal-ai/client";

const file = new File(["Hello, World!"], "hello.txt", { type: "text/plain" });
const url = await fal.storage.upload(file);
```

##### Auto uploads

The client will auto-upload the file for you if you pass a binary object (e.g. `File`, `Data`).

Read more about file handling in our [file upload guide](https://docs.fal.ai/model-endpoints#file-uploads).

## 5. Schema[#](#schema)

### Input[#](#schema-input)

`prompt` `string`\* required

The prompt to generate an image from.

`seed` `integer`

The same seed and the same prompt given to the same version of the model
will output the same image every time.

`guidance_scale` `float`

The CFG (Classifier Free Guidance) scale is a measure of how close you want
the model to stick to your prompt when looking for a related image to show you. Default value: `3.5`

`sync_mode` `boolean`

If set to true, the function will wait for the image to be generated and uploaded
before returning the response. This will increase the latency of the function but
it allows you to get the image directly in the response without going through the CDN.

`num_images` `integer`

The number of images to generate. Default value: `1`

`safety_tolerance` `SafetyToleranceEnum`

API only

The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: `"2"`

Possible enum values: `1, 2, 3, 4, 5, 6`

**Note:** This property is only available through API calls.

`output_format` `OutputFormatEnum`

The format of the generated image. Default value: `"jpeg"`

Possible enum values: `jpeg, png`

`aspect_ratio` `AspectRatioEnum`

The aspect ratio of the generated image.

Possible enum values: `21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21`

`image_url` `string`\* required

Image prompt for the omni model.

```
{
  "prompt": "Put a donut next to the flour.",
  "guidance_scale": 3.5,
  "num_images": 1,
  "safety_tolerance": "2",
  "output_format": "jpeg",
  "image_url": "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
}
```

### Output[#](#schema-output)

`images` `list<[fal__toolkit__image__image__Image](#type-fal__toolkit__image__image__Image)>`\* required

The generated image files info.

`timings` `[Timings](#type-Timings)`\* required

`seed` `integer`\* required

Seed of the generated Image. It will be the same value of the one passed in the
input or the randomly generated that was used in case none was passed.

`has_nsfw_concepts` `list<[boolean](#type-boolean)>`\* required

Whether the generated images contain NSFW concepts.

`prompt` `string`\* required

The prompt used for generating the image.

```
{
  "images": [
    {
      "height": 1024,
      "url": "https://fal.media/files/tiger/7dSJbIU_Ni-0Zp9eaLsvR_fe56916811d84ac69c6ffc0d32dca151.jpg",
      "width": 1024
    }
  ],
  "prompt": ""
}
```

### Other types[#](#schema-other)

#### registry\_\_image\_\_fast\_sdxl\_\_models\_\_Image[#](#type-registry__image__fast_sdxl__models__Image)

`url` `string`\* required

`width` `integer`\* required

`height` `integer`\* required

`content_type` `string`

Default value: `"image/jpeg"`

#### FluxProRedux[#](#type-FluxProRedux)

`prompt` `string`

The prompt to generate an image from. Default value: `""`

`image_size` `[ImageSize](#type-ImageSize) | [Enum](#type-Enum)`

The size of the generated image. Default value: `landscape_4_3`

Possible enum values: `square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9`

**Note:** For custom image sizes, you can pass the `width` and `height` as an object:

```
"image_size": {
  "width": 1280,
  "height": 720
}
```

`num_inference_steps` `integer`

The number of inference steps to perform. Default value: `28`

`seed` `integer`

The same seed and the same prompt given to the same version of the model
will output the same image every time.

`guidance_scale` `float`

The CFG (Classifier Free Guidance) scale is a measure of how close you want
the model to stick to your prompt when looking for a related image to show you. Default value: `3.5`

`sync_mode` `boolean`

If set to true, the function will wait for the image to be generated and uploaded
before returning the response. This will increase the latency of the function but
it allows you to get the image directly in the response without going through the CDN.

`num_images` `integer`

The number of images to generate. Default value: `1`

`safety_tolerance` `SafetyToleranceEnum`

API only

The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: `"2"`

Possible enum values: `1, 2, 3, 4, 5, 6`

**Note:** This property is only available through API calls.

`output_format` `OutputFormatEnum`

The format of the generated image. Default value: `"jpeg"`

Possible enum values: `jpeg, png`

`image_url` `string`\* required

The image URL to generate an image from. Needs to match the dimensions of the mask.

#### FluxProV1Redux[#](#type-FluxProV1Redux)

`prompt` `string`

The prompt to generate an image from. Default value: `""`

`image_size` `[ImageSize](#type-ImageSize) | [Enum](#type-Enum)`

The size of the generated image. Default value: `landscape_4_3`

Possible enum values: `square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9`

**Note:** For custom image sizes, you can pass the `width` and `height` as an object:

```
"image_size": {
  "width": 1280,
  "height": 720
}
```

`num_inference_steps` `integer`

The number of inference steps to perform. Default value: `28`

`seed` `integer`

The same seed and the same prompt given to the same version of the model
will output the same image every time.

`guidance_scale` `float`

The CFG (Classifier Free Guidance) scale is a measure of how close you want
the model to stick to your prompt when looking for a related image to show you. Default value: `3.5`

`sync_mode` `boolean`

If set to true, the function will wait for the image to be generated and uploaded
before returning the response. This will increase the latency of the function but
it allows you to get the image directly in the response without going through the CDN.

`num_images` `integer`

The number of images to generate. Default value: `1`

`safety_tolerance` `SafetyToleranceEnum`

API only

The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: `"2"`

Possible enum values: `1, 2, 3, 4, 5, 6`

**Note:** This property is only available through API calls.

`output_format` `OutputFormatEnum`

The format of the generated image. Default value: `"jpeg"`

Possible enum values: `jpeg, png`

`image_url` `string`\* required

The image URL to generate an image from. Needs to match the dimensions of the mask.

#### fal\_\_toolkit\_\_image\_\_image\_\_Image[#](#type-fal__toolkit__image__image__Image)

`url` `string`\* required

The URL where the file can be downloaded from.

`content_type` `string`

The mime type of the file.

`file_name` `string`

The name of the file. It will be auto-generated if not provided.

`file_size` `integer`

The size of the file in bytes.

`file_data` `string`

File data

`width` `integer`

The width of the image in pixels.

`height` `integer`

The height of the image in pixels.

#### FluxProUltraTextToImageInputRedux[#](#type-FluxProUltraTextToImageInputRedux)

`prompt` `string`

The prompt to generate an image from. Default value: `""`

`seed` `integer`

The same seed and the same prompt given to the same version of the model
will output the same image every time.

`sync_mode` `boolean`

If set to true, the function will wait for the image to be generated and uploaded
before returning the response. This will increase the latency of the function but
it allows you to get the image directly in the response without going through the CDN.

`num_images` `integer`

The number of images to generate. Default value: `1`

`enable_safety_checker` `boolean`

If set to true, the safety checker will be enabled. Default value: `true`

`safety_tolerance` `SafetyToleranceEnum`

API only

The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: `"2"`

Possible enum values: `1, 2, 3, 4, 5, 6`

**Note:** This property is only available through API calls.

`output_format` `OutputFormatEnum`

The format of the generated image. Default value: `"jpeg"`

Possible enum values: `jpeg, png`

`aspect_ratio` `[Enum](#type-Enum) | [string](#type-string)`

The aspect ratio of the generated image. Default value: `16:9`

Possible enum values: `21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21`

`raw` `boolean`

Generate less processed, more natural-looking images.

`image_url` `string`\* required

The image URL to generate an image from. Needs to match the dimensions of the mask.

`image_prompt_strength` `float`

The strength of the image prompt, between 0 and 1. Default value: `0.1`

#### ImageSize[#](#type-ImageSize)

`width` `integer`

The width of the generated image. Default value: `512`

`height` `integer`

The height of the generated image. Default value: `512`

#### FluxProTextToImageInputWithAR[#](#type-FluxProTextToImageInputWithAR)

`prompt` `string`\* required

The prompt to generate an image from.

`seed` `integer`

The same seed and the same prompt given to the same version of the model
will output the same image every time.

`guidance_scale` `float`

The CFG (Classifier Free Guidance) scale is a measure of how close you want
the model to stick to your prompt when looking for a related image to show you. Default value: `3.5`

`sync_mode` `boolean`

If set to true, the function will wait for the image to be generated and uploaded
before returning the response. This will increase the latency of the function but
it allows you to get the image directly in the response without going through the CDN.

`num_images` `integer`

The number of images to generate. Default value: `1`

`safety_tolerance` `SafetyToleranceEnum`

API only

The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: `"2"`

Possible enum values: `1, 2, 3, 4, 5, 6`

**Note:** This property is only available through API calls.

`output_format` `OutputFormatEnum`

The format of the generated image. Default value: `"jpeg"`

Possible enum values: `jpeg, png`

`aspect_ratio` `AspectRatioEnum`

The aspect ratio of the generated image. Default value: `"1:1"`

Possible enum values: `21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21`

## Related Models

#### Learn More

[Status](https://status.fal.ai)[Documentation](https://docs.fal.ai)[Pricing](/pricing)[Enterprise](/enterprise)[Grants](/grants)[About Us](/about)[Careers](/careers)[Blog](https://blog.fal.ai)[Get in touch](/cdn-cgi/l/email-protection#483b3d3838273a3c082e2924662921)

Models[AuraFlow](/models/fal-ai/aura-flow)[Flux.1 [schnell]](/models/fal-ai/flux/schnell)[Flux.1 [dev]](/models/fal-ai/flux/dev)[Flux Realism LoRA](/models/fal-ai/flux-realism)[Flux LoRA](/models/fal-ai/flux-lora)[Explore More](/models)

#### Playgrounds

[Training](/models/fal-ai/flux-lora-fast-training)[Workflows](/workflows)[Demos](/demos)

#### Socials

[Discord](https://discord.gg/fal-ai)[GitHub](https://github.com/fal-ai)[Twitter](https://twitter.com/fal)[Linkedin](https://www.linkedin.com/company/features-and-labels/)

features and labels, 2025. All Rights Reserved. [Terms of Service](/terms.html) and [Privacy Policy](/privacy.html)
