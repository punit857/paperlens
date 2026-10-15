<div align="center">

# PaperLens

**Turn an ML paper abstract into structured JSON with a small, fine-tuned language model.**

[![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-Hugging%20Face-yellow)](https://huggingface.co/punit-09/paperlens-qwen2.5-3b-qlora)
[![Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-Hugging%20Face-orange)](https://huggingface.co/datasets/punit-09/paperlens-arxiv-abstracts)
[![Code license](https://img.shields.io/badge/code%20license-MIT-green)](LICENSE)

</div>

I fine-tuned **Qwen2.5-3B** with QLoRA to read a paper's title and abstract and return its **task, method, datasets, metrics, main result and contribution type**, using only a free Kaggle GPU.

On 150 held-out abstracts it scores **0.87** overall, compared with **0.77** for a 20B-parameter model given the same labeling rules and **0.66** for the untuned base model.

## Results

![Overall score](docs/macro.png)

**Score per field** (0 to 1, higher is better)

| Field | Qwen2.5-3B + prompt | gpt-oss-20b + rules | **PaperLens** |
|---|:---:|:---:|:---:|
| Task | 0.53 | 0.60 | **0.81** |
| Method | 0.67 | 0.69 | **0.78** |
| Datasets | 0.64 | 0.89 | **0.93** |
| Metrics | 0.59 | 0.80 | **0.91** |
| Contribution type | 0.87 | 0.91 | **0.97** |
| Main result | 0.67 | 0.75 | **0.81** |
| **Overall** | 0.66 | 0.77 | **0.87** |

**Reliability**

| | Qwen2.5-3B + prompt | gpt-oss-20b + rules | **PaperLens** |
|---|:---:|:---:|:---:|
| Valid JSON output | 98% | 99% | **100%** |
| Datasets/metrics not found in the abstract | 10.0% (26/261) | 5.6% (9/161) | **0.0% (0/118)** |

Scores measure agreement with LLM-generated reference labels, not human ground truth, and PaperLens was trained in the same labeling style. 30 of the 150 test rows were reviewed by me. gpt-oss-20b is shown with the better of the two prompts I tried. On datasets, the gap to it is within statistical noise.

## Example

**Title:** *Longer is (Not Necessarily) Stronger: Punctuated Long-Sequence Training for Enhanced Speech Recognition and Translation*

**Abstract (shortened):** *This paper presents a new method for training sequence-to-sequence models for speech recognition and translation tasks. Instead of the traditional approach of training models on short segments containing only lowercase or partial punctuation and capitalization (PnC) sentences, we propose training on longer utterances that include ...*

```json
{
  "task": "speech recognition and translation",
  "method": "punctuated long-sequence training",
  "datasets": [
    "Earnings-21",
    "Earnings-22"
  ],
  "metrics": [
    "WER"
  ],
  "main_result": "Training on sequences longer than 40 seconds shows a 25% relative word error rate improvement on the Earnings-21 and Earnings-22 benchmarks.",
  "contribution_type": "new_method"
}
```

## How it works

![Pipeline](docs/pipeline.png)

## Limitations

- Labels are LLM-generated and contain errors; their noise rate is unmeasured.
- One training run on English ML abstracts from three arXiv categories. Other fields are untested.
- About 13 seconds per abstract on a T4 (4-bit model with an unmerged adapter), so this setup is not tuned for speed.

## Links

[Model](https://huggingface.co/punit-09/paperlens-qwen2.5-3b-qlora) · [Dataset and results](https://huggingface.co/datasets/punit-09/paperlens-arxiv-abstracts) · [Full pipeline notebook](notebooks/paperlens.ipynb)

Code is MIT-licensed. The model is **Improved using Qwen** and released under the Qwen Research License (non-commercial use only). Labels were generated with the Gemini API; check Google's terms before reusing them.
