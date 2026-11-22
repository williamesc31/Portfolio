# Invoice Extraction and Arithmetic Validation

Convert a documented invoice text layout into structured JSON and reject inconsistent totals.

## Question

Can invoice fields and line items be extracted into a consistent structure with verifiable arithmetic?

## Approach

Use anchored field extraction, an explicit quantity/description/unit-price grammar, ISO date checks, and Decimal arithmetic. Process three fictional valid fixtures and verify that a deliberately inconsistent total is rejected. Return structured JSON for a supplied text file.

## Reproduce

From the repository root, using Python 3.12:

```bash
python -m pip install -r requirements.txt
python projects/invoice-extraction/analyze.py
```

The default command uses bundled snapshots, writes `outputs/results.json`, and requires no API key, GPU, or live data service. Shared chart and JSON helpers are in `projects/common.py`.

## Verified results

All 3 valid fictional fixtures were processed, and the inconsistent-total fixture was rejected. These are regression checks for supported layouts, not a real-world extraction benchmark.

The saved machine-readable results are in [outputs/results.json](outputs/results.json). Repository-wide execution evidence and input/code hashes are in [VERIFICATION.json](../../VERIFICATION.json).

## Interpretation and limitations

A schema and arithmetic checks make extraction errors visible. This release supports a defined text layout and does not claim OCR, arbitrary-layout handling, or LLM benchmark performance.

## Data and provenance

A new local portfolio implementation based on earlier invoice-extraction coursework. The bundled invoices are explicitly fictional fixtures created for regression checks. The earlier paid-API notebook is not required or represented as tested in this release.

## Tools

Python · Regular expressions · Decimal · Data validation

To parse another supported text invoice, pass `--input path/to/invoice.txt`. Input fields and the line-item layout are demonstrated in `data/invoice_001.txt`. Invalid or inconsistent inputs raise a clear error.
