# Human Models

[Human main repository](https://github.com/vladmandic/human)  

For model details and credits see [documentation in the main library](https://github.com/vladmandic/human/wiki/Models)  

Default models are included in the main library  

Optional models are published here to keep the size of the main library contained  

## Usage

`Human` includes default models but supports number of additional models and model variations of existing models  

Additional models can be accessed via:
 - [GitHub repository](https://github.com/vladmandic/human-models)
 - [NPMjs package](https://www.npmjs.com/package/@vladmandic/human-models)
 - [jsDelivr CDN](https://www.jsdelivr.com/package/npm/@vladmandic/human-models)

You can manually download models and update configuration `modelPath` value to each model or simply set `baseModelPath` to this list  
To use online CDN, simply set `human.config.baseModelPath` to `https://www.jsdelivr.com/package/npm/@vladmandic/human-models/models`

<br>

## List of Included Models

Pose detection alternatives
- `movenet-lightning`
- `movenet-thunder`
- `movenet-multipose`
- `efficientpose`
- `posenet`
- `blazepose-lite`
- `blazepose-full`
- `blazepose-heavy`

HandPose and HandTrack family:
- `handdetect`
- `handtrack`
- `handskeleton`
- `handlandmark-full`
- `handlandmark-lite`
- `handlandmark-sparse`

Object detection:
- `mb3-centernet`
- `nanodet`

Segmentation:
- `meet`
- `selfie`

Face analysis:
- `blazeface`
- `blazeface-back`
- `blazeface-front`
- `age`
- `emotion`
- `faceboxes`
- `facemesh`
- `faceres`
- `faceres-deep`
- `gear`
- `gender`
- `gender-ssrnet-imdb`
- `iris`
- `liveness`
- `mobileface`
- `mobilefacenet`
