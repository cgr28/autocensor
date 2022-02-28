# Auto Censor
A command-line program that utilizes OpenCV and Tesseract to censor a given set of words from an image or directory of images.
**Tools used:** Python, Tesseract, OpenCV
## Pre-requisites
- [Tesseract](https://github.com/tesseract-ocr/tesseract) installed.
- All modules in the requirements.txt installed.

## How to
#### Change minimum confidence
To change the minimum confidence, change the value of the *min_conf* variable (line 22), to any value between 0 and 100.
```python
min_conf = 1.0 # can be anything between 0 and 100
```
#### Change censor words
To select words to censor, edit the *wordstocensor.txt* file.  Follow each word with a newline. Leave **empty** to censor all words.
```text
enter
the
words
in
this
format
```

#### Run the program
In the autocensor directory call the *main program* followed by the *path to the image* or *directory of images* you want censored. To change the censor style, provide the argument **black** for black censor bars or **white** for white censor bars.
```console
python main.py {path to image/directory} {black/white}
```

#### Output
The words that were censored and their respective confidence, will be recorded in the *censorreport.txt* file. The censored images will be place in a *censoredimgs* directory that the script will create.

## Example
For this example the words best, times, and foolishness will be censored from *example.png*.
<p>
    <img src="https://raw.githubusercontent.com/cgr28/autocensor/main/example.png" alt="example"/>
    <em>the image example.png before being censored</em>
</p>

1. Edit *wordstocensor.txt* to include the words that need to be cesnored
   ```text
   best
   times
   foolishness
   ```
2. Run the script to censor the words.
   ```console
   python main.py example.png
   ```
<p>
    <img src="https://raw.githubusercontent.com/cgr28/autocensor/main/censor-example.png" alt="example"/>
    <em>the censored image in censoredimgs/censored-example.png</em>
</p>