# Financial Sentiment Analysis with Generative AI

## Overview

This project classifies financial statements and headlines as positive, neutral, or negative through an interactive Streamlit application.

## Development

Prompt experiments examined task instructions, examples, and response formats. The initial OpenAI fine-tuning plan could not be completed because of access limitations. Development moved to Together AI and LoRA. A training dataset was prepared, validated, and uploaded, and an adapter was created. Serving challenges required additional testing in Google Colab; the application was later rebuilt.

## Application and model status

The Streamlit interface accepts financial text and displays a sentiment label. The active model backend of the rebuilt application and the availability of the training artifacts must be confirmed before publishing the code. Historical adapter training does not by itself identify the current application backend.

## Evaluation

No verified benchmark accuracy is reported in this draft. A labeled holdout set should support per-class precision, recall, F1-score, and a confusion matrix. Prompt-based and adapted-model comparisons should use the same test data.

## Reproduction status

The repository URL, application entry point, dependency versions, startup command, provider configuration, and active model identifier will be added after verification. Credentials must be configured outside the repository. Application checks should cover empty input, service errors, unexpected output, and all supported labels.

## Tools

Python, large language models, LoRA, Together AI, REST APIs, Streamlit, Google Colab. OpenAI was part of the original workflow design.

## Lessons and next steps

Training and serving are separate tasks. Reproducibility depends on saving configuration, dependencies, and model artifacts. Future work could include systematic benchmarking, batch processing, and financial entity extraction. Mixed sentiment and limited context remain important limitations.
