# cochl-sense-py

## Installation

```python
pip install cochl
```

## Usage

### File Usage

This simple setup is enough to infer your file:
```python
from cochl.file import FileClient

client = FileClient(
    api_project_key="your_api_project_key",
)

results = client.predict("your_file.wav")
print(results.to_dict()) # get results as a dict
```

Some parameters can be adjusted, and you can read about them in the documentation
```python
from cochl import config
from cochl.file import FileClient

api_config = config.APIConfig(
    window_hop=config.WindowHop.HOP_1s,
    sensitivity=config.SensitivityConfig(
        interval_margin=config.SensitivityScale.VERY_HIGH,
        by_tags={"Siren": config.SensitivityScale.LOW}
    ),
)

client = FileClient(
    api_project_key="your_api_project_key",
)

results = client.predict("your_file.wav")
print(results.to_dict()) # get results as a dict
```

When you opt for the "abbreviated results" display, you can also choose how to deal with the interval margins
```python
print(results.to_summarized_result(
    hop_size=config.WindowHop.HOP_500ms,
    interval_margin=2,
    by_tags={"Speech": 5, "Sing": 3}
)) # get results in a simplified format
```

### Convert to supported file formats (WAV, MP3, OGG)

If a file is not in a supported format (WAV, MP3, OGG), then it has to be manually converted to one of the supported formats. \
`Pydub` is one of the ways to do so.

First install Pydub refering to this [link](https://github.com/jiaaro/pydub?tab=readme-ov-file#installation). \
Then write a Python script converting your file into a supported format like below.

```python
from pydub import AudioSegment

mp4_version = AudioSegment.from_file("sample.mp4", "mp4")
mp4_version.export("sample.mp3", format="mp3")
```

For more details of `Pydub`, please refer to this [link](https://github.com/jiaaro/pydub)


## Advanced Configurations

### Audio Window

Cochl.Sense analyzes audio data in "window" unit, which is a block of audio data with fixed length in time. \
For example, there are two windows in a 2.0 second audio file like below when **window size** is 1 second.

- Window #0 (0.0s ~ 1.0s)
- Window #1 (1.0s ~ 2.0s)


Window size is fixed to 1 second.

### Window Hop

"Window Hop" represents the gap between consecutive audio windows.

When the value of **window hop** is equal to **window size**, all audio windows have no overlap.
They are contiguous to each other. \
For example, when `WindowSize=1.0s` and `WindowHop=1.0s`, there are two audio windows for 2.0 second file like below.

- Window #0 (0.0s ~ 1.0s)
- Window #1 (1.0s ~ 2.0s)

When **window hop** is smaller than **window size**, audio windows overlap each other. \
For example, when `WindowSize=1.0s` and `WindowHop=0.5s`, there are two audio windows for 2.0 second file like below.

- Window #0' (0.0s ~ 1.0s)
- Window #1' (0.5s ~ 1.5s)
- Window #2' (1.0s ~ 2.0s)

The smaller **window hop** makes prediction slower, because it results in more windows to predict. \
But it can reduce the possibility of missing sounds between two different windows. \
For example, one wants to detect "Gunshot", and it's recorded in the range of `0.9s ~ 1.1s`.
It's possbily not detected when `WindowHop=1.0s` because the sound is separted into two different windows: `Window #0` and `Window #1`. \
However, when `WindowHop=0.5s`, the "Gunshot" sound is placed in the middle of `Window #1' (0.5s ~ 1.5s)`. \

To adjust window hop in the code, you can follow the sample below. \
The default value is `0.5s`.

```python
import cochl.sense as sense

api_config = sense.APIConfig(
    window_hop=sense.WindowHop.HOP_1s,
)
client = sense.FileClient(
    "YOUR_API_PROJECT_KEY",
    api_config=api_config,
)
```

### Sensitivity

You can adjust how sensitive each sound tag should be detected. \
High sensitivity makes Cochl.Sense determine a sound tag is detected even though its confidence is low.

For example, let's imagine Cochl.Sense determine "Gunshot" is detected only when inference result says there is "Gunshot" with 0.3 (30%) confidency. \
When inferece result of "Gunshot" is 0.29 confidency, then Cochl.Sense responses no "Gunshot". \
However, when the sensitivity for "Gunshot" is set HIGH, then Cochl.Sense determines "Gunshot" is detected.

To adjust sensitivity in the code, you can follow the sample below.
The default value is `MEDIUM`.
```python
import cochl.sense as sense

api_config = sense.APIConfig(
    sensitivity=sense.SensitivityConfig(
        # default sensitivity applied to all tags not specified in `by_tags`
        default=sense.SensitivityScale.LOW,
        by_tags={
            "Baby_cry": sense.SensitivityScale.VERY_LOW,
            "Gunshot":  sense.SensitivityScale.HIGH,
        },
    ),
)
client = sense.FileClient(
    "YOUR_API_PROJECT_KEY",
    api_config=api_config,
)
```


## Links

Documentation: https://docs.cochl.ai/sense/api/
