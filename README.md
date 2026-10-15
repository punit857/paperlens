<div align="center">

# PaperLens

### Turning research abstracts into structured, machine-readable knowledge.

Fine-tune a small language model to extract research tasks, methods, datasets, metrics, results, and contribution types from machine learning paper abstracts.

**0.87 Overall Score** · **100% Valid JSON** · **3B-Parameter Model**

[**Model**](https://huggingface.co/punit-09/paperlens-qwen2.5-3b-qlora) · [**Dataset**](https://huggingface.co/datasets/punit-09/paperlens-arxiv-abstracts) · [**Training Notebook**](notebooks/paperlens.ipynb)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![QLoRA](https://img.shields.io/badge/Fine--tuning-QLoRA-blue?style=flat-square)
![License](https://img.shields.io/badge/Code-MIT-green?style=flat-square)

</div>

---

## The problem

Research papers contain valuable information, but extracting it into a consistent structure is tedious. Important details such as datasets, evaluation metrics, and reported results are expressed differently across papers.

**PaperLens explores whether a small, fine-tuned language model can automate this extraction task.**

Given a paper's title and abstract, PaperLens produces structured JSON containing six fields:

| Field | What it captures |
|---|---|
| `task` | The research problem being addressed |
| `method` | The proposed approach or technique |
| `datasets` | Datasets mentioned in the abstract |
| `metrics` | Evaluation metrics reported |
| `main_result` | The main finding or quantitative result |
| `contribution_type` | The type of research contribution |

## Results at a glance

Evaluated on **150 held-out abstracts**, PaperLens achieved an overall score of **0.87**, outperforming the two reported baselines.

![Overall evaluation score comparing PaperLens with two baselines](docs/macro.png)

### Field-level evaluation

Scores range from 0 to 1; higher indicates greater agreement with the reference labels.

| Field | Qwen2.5-3B + schema prompt | gpt-oss-20b + labeling rules | **PaperLens** |
|:---|:---:|:---:|:---:|
| Task | 0.53 | 0.60 | **0.81** |
| Method | 0.67 | 0.69 | **0.78** |
| Datasets | 0.64 | 0.89 | **0.93** |
| Metrics | 0.59 | 0.80 | **0.91** |
| Contribution type | 0.87 | 0.91 | **0.97** |
| Main result | 0.67 | 0.75 | **0.81** |
| **Overall** | **0.66** | **0.77** | **0.87** |

### Output reliability

| Measure | Qwen2.5-3B + schema prompt | gpt-oss-20b + labeling rules | **PaperLens** |
|:---|:---:|:---:|:---:|
| Valid JSON output | 98% | 99% | **100%** |
| Unsupported dataset/metric mentions when absent from abstract | 10.0% (26/261) | 5.6% (9/161) | **0.0% (0/118)** |

**How to interpret these results:** Scores measure agreement with LLM-generated reference labels, not independently verified human ground truth. PaperLens was trained using the same labeling style. I manually reviewed 30 of the 150 test examples. The larger model's result reflects the better of two prompts tested, and the dataset comparison gap is within statistical noise.

## How it works

![PaperLens training and evaluation pipeline](docs/pipeline.png)

1. **Collect:** Gather 1,749 arXiv abstracts from `cs.LG`, `cs.CL`, and `cs.CV`.
2. **Label:** Generate structured labels using the Gemini API and check them with code.
3. **Fine-tune:** Adapt Qwen2.5-3B using QLoRA on a free Kaggle T4 GPU, with a reported training time of approximately 30 minutes.
4. **Evaluate:** Test on 150 held-out papers and report field-level scores and 95% confidence intervals.
5. **Release:** Publish the model and dataset on Hugging Face.

## Example output

**Paper:** *Longer is (Not Necessarily) Stronger: Punctuated Long-Sequence Training for Enhanced Speech Recognition and Translation*

**Input:** The paper's title and abstract, describing long-sequence training for speech recognition and translation.

**Extracted JSON:**

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

*The example illustrates the output format; extracted claims should still be checked against the original paper.*

## Reproducibility and artifacts

Explore the released artifacts to inspect the model, dataset, and training workflow.

- **Fine-tuned model:** [PaperLens on Hugging Face](https://huggingface.co/punit-09/paperlens-qwen2.5-3b-qlora)
- **Dataset and evaluation results:** [PaperLens dataset on Hugging Face](https://huggingface.co/datasets/punit-09/paperlens-arxiv-abstracts)
- **Training and evaluation notebook:** [Open `paperlens.ipynb`](notebooks/paperlens.ipynb)

The notebook is the starting point for examining the training and evaluation workflow. Consult it and the model documentation for the exact dependencies, loading procedure, and inference interface.

## Limitations

- **Reference-label quality:** Labels were generated by an LLM and may contain errors. The overall label noise rate has not been measured.
- **Limited evaluation scope:** The experiment covers English abstracts from three arXiv categories, with one reported training run.
- **Inference latency:** Inference takes approximately 13 seconds per abstract on a T4 using a 4-bit model with an unmerged adapter. This setup has not been optimized for speed.
- **Not a verified knowledge source:** The model can omit, misinterpret, or incorrectly extract claims. Outputs should be validated before use in downstream research workflows.

## Future directions

Potential next steps include:

- Expanding evaluation across more research domains and datasets.
- Improving reference-label quality through broader human review.
- Evaluating robustness to ambiguous abstracts and missing information.
- Optimizing inference latency and measuring performance across multiple training runs.

## License and attribution

- **Code:** MIT license. See [`LICENSE`](LICENSE).
- **Model:** Fine-tuned from Qwen2.5-3B. The released model is identified as improved using Qwen and is subject to the Qwen Research License, which restricts commercial use. Review the applicable license before deployment.
- **Dataset:** Labels were generated using the Gemini API. Check the applicable terms before reusing or redistributing the labeled data.

---

<div align="center">

**PaperLens** — exploring practical, resource-efficient extraction of structured knowledge from research papers.

[Model](https://huggingface.co/punit-09/paperlens-qwen2.5-3b-qlora) · [Dataset](https://huggingface.co/datasets/punit-09/paperlens-arxiv-abstracts) · [Notebook](notebooks/paperlens.ipynb)

</div>
