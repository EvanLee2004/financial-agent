# AutoCPA

**AutoCPA** is a local-first, AI-powered financial analysis tool designed for Chinese public company Annual Reports (PDFs).

## Features

- **Local-First**: Runs entirely on your machine (macOS M3 Max optimized).
- **AI-Powered**: Uses Qwen2.5-VL for intelligent visual extraction.
- **Financial Analysis**: Automated calculation of key financial ratios using `FinanceToolkit`.
- **Validation**: Strict accounting equation checks (`Assets = Liabilities + Equity`).

## Architecture

- **Frontend**: Streamlit
- **Core**: Python (Pydantic, pdfplumber, OpenAI SDK)
- **AI Backend**: Local Qwen2.5-VL via LM Studio/Ollama

## Usage

1. Upload a PDF Annual Report.
2. AutoCPA identifies key financial statements.
3. Data is extracted, audited, and analyzed.
4. View interactive dashboard and download reports.
