import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import sys
import os
import string

# create a dir to store imgs if it dne
if not os.path.exists("./censoredimgs"):
    os.makedirs("./censoredimgs")

cens_all = False # if set to true all words will be censored
cens_words = set() # words that will be censored
words = open("wordstocensor.txt", "r").readlines()
out = open("censorreport.txt", "w")
num_words = 0 # total num of words
num_cens = 0 # num of words censored
imgs = [] # contains all images
black = False # when True censor bars will be black
white = False # when True censor bars will be white

try:
    if sys.argv[2] == "black":
        black = True
    elif sys.argv[2] == "white":
        white = True
except:
    pass
    

if words:
    for word in words:
        cens_words.add(word.strip("\n"))
else:
    cens_all = True

path = sys.argv[1]

if os.path.isfile(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    imgs.append([img, path])
elif os.path.isdir(path):
    for file in os.listdir(path):
        if os.path.isfile(f"{path}/{file}"):
            try:
                img = cv2.imread(f"{path}/{file}", cv2.IMREAD_COLOR)
                imgs.append([img, file])
            except:
                print("Couldn't open ", file, ".")
else:
    print("Error.")
    sys.exit()

for img, f in imgs:

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(img_rgb, output_type=Output.DICT)

    out.write(f"IMAGE: {f}\n\n")

    for i in range(len(results["text"])):

        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]

        text = results["text"][i]
        conf = float(results["conf"][i])

        if conf > 1:
            num_words += 1
            text = text.strip(string.punctuation).lower() # cleaning text by removing leading/trailing punctuation and setting to lowercase
            # creating blur rect
        
            if black:
                cens = np.zeros([h, w, 3], dtype=int)
            elif white:
                cens = np.full([h, w, 3], 255)
            else:
                cens = img[y:y+h, x:x+w]
                cens = cv2.GaussianBlur(cens, (23, 23), 30)

            if cens_all:
                out.write(f"\tcensored {text.upper()} with {conf}% confidence\n")
                img[y:y+cens.shape[0], x:x+cens.shape[1]] = cens
                num_cens += 1
            elif text in cens_words:
                out.write(f"\tcensored {text.upper()} with {conf}% confidence\n")
                img[y:y+cens.shape[0], x:x+cens.shape[1]] = cens
                num_cens += 1
    cv2.imwrite(f"./censoredimgs/censored-{f}", img)
    perc = "%.2f" % (num_cens/num_words * 100)
    out.write(f"\ncensored {perc}% ({num_cens}/{num_words}) of words\n\n")

print("complete.")