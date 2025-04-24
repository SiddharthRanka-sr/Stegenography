# Text-in-Image Steganography

This project implements a basic steganography system in Python to hide secret text messages within images. The goal is to provide a simple yet effective technique to embed and extract hidden messages using image files.

---

## Features

- Hide (encode) text messages inside image files
- Extract (decode) hidden messages from stego images
- Supports common image formats (PNG, JPG)
- Output file is generated as `hidden.png`
- Written entirely in Python

---

## Requirements

- Python 3.x (recommended: Python 3.8 or later)

---

## Installation
```bash
pip install pillow
pip install pycryptodome
```
### Usage
Encode Text into Image
```bash
python enc.py 
```
You will be prompted to enter the message you want to hide.
A new image file named hidden.png will be created with the embedded message.

Decode Text from Image
```bash
python dec.py 
```
