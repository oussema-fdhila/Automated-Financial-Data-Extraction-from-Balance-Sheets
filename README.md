# Automated Financial Data Extraction from Balance Sheets

## Project Overview

This project aims to automate the extraction of key financial data from digitized balance sheets using Optical Character Recognition (OCR) and image processing techniques. The goal is to reduce manual data entry, minimize errors, and accelerate the financial analysis process by efficiently extracting relevant information such as assets, liabilities, and results from scanned balance sheets.

## Key Features

- **OCR-based Extraction**: Uses Tesseract OCR (via Pytesseract) to extract textual information from images of balance sheets.
- **Image Preprocessing**: Implements advanced image preprocessing techniques such as contrast adjustment, resizing, and binarization to optimize the accuracy of text extraction.
- **Data Filtering**: Filters extracted text to retain only key financial terms and values, such as "Assets," "Liabilities," "Equity," and "Results."

## Technologies Used

- **Python**: The main programming language for automation and data extraction.
- **Pytesseract**: OCR tool for extracting text from images.
- **Pillow (PIL)**: Python Imaging Library used for image preprocessing (grayscale conversion, contrast adjustment, resizing, etc.).
- **Regular Expressions**: Used for filtering and processing extracted text.

## Project Goal

The goal of this project is to build an automated system for extracting relevant financial data from scanned balance sheets. The system is designed to handle different document formats and qualities by applying image processing techniques that improve OCR accuracy.

## Current Stage

The project is currently in the **implementation phase**. The following steps have been completed:

- The OCR system has been implemented using Pytesseract.
- Basic image preprocessing steps (contrast adjustment, resizing, and binarization) have been integrated.
- Initial tests have been conducted to extract key financial data.

### Next Steps

- Refine the image preprocessing steps to ensure optimal results for different types of documents.
- Test the system with a larger set of balance sheets for validation.
- Add further enhancements to improve accuracy and handle edge cases.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/oussema-fdhila/Automated-Financial-Data-Extraction-from-Balance-Sheets.git
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Install Tesseract OCR (if not already installed):
   - **Windows**: Download the installer from https://github.com/UB-Mannheim/tesseract/wiki .
   - **macOS**: Use Homebrew:
     ```bash
     brew install tesseract
   - **Linux**: Install via package manager:
     ```bash
     sudo apt-get install tesseract-ocr
4. Run the script to extract data from a balance sheet image:
   ```bash
   python extract_data.py --image path_to_image.png

## Contributors
   - **Oussama Fdhila** - Project Lead - Data Scientist
   - **M. Ahmed Filali** - Technical Supervisor

