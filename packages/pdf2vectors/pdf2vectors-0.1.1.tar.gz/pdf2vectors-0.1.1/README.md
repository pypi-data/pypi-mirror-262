# pdf2vectors


## Description

This package provides a convenient way to interact with a vectors database using Pinecone, allowing you to upload data in the form of vectors to your Pinecone index.


## Installation

You can install the package via pip:

```bash
pip install pdf2vectors
```


## Usage

```python
from pdf2vectors import PineconeUploader, read_pdf, upsert_files

PineconeUploader(api_key="YOUR_PINECONE_API_KEY", host="YOUR_PINECONE_HOST")

directory = "YOUR_PDF_FILE_PATH"
texts = read_pdf(directory)

response = upsert_files(texts)

print(response)
```

## Features

Simplified Interaction: Easily upload vectorized data to your Pinecone index with just a few lines of code.
Automatic Vectorization: The package automatically vectorizes text content extracted from PDF files.
Flexible Configuration: Customize the package by providing your Pinecone API key and host.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the functionality or fix any bugs in the package. Your contributions help improve the overall quality of the package and make it more valuable for the community.