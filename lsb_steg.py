#!/bin/env python3

from PIL import Image, ImageFont
from PIL import ImageDraw
import textwrap
import sys


def getitem(item):
    try:
        img = Image.open(item)
    except IOError as e:
        print("[ ! ] error accessing file : {}".format(e))
        sys.exit()
    return img


def setitem(img, outfile):
    try:
        img.save(outfile)
    except IOError as e:
        print(" [ ! ] image could not be written : {}".format(e))
        sys.exit()
    except Exception as e:
        print(" [ ! ] unable to save : {}".format(e))
        sys.exit()


def create_text_image(text, img_size):
    img_text = Image.new("RGB", img_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(img_text)
    margin = offset = 10
    for line in textwrap.wrap(text, width=int(img_size[0] / 9)):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return img_text


def decode_text(steg_img_path, outfile):
    steg_img = getitem(steg_img_path)
    red_channel = steg_img.split()[0]

    x_size = steg_img.size[0]
    y_size = steg_img.size[1]

    decoded_img = Image.new("RGB", steg_img.size)
    pixels = decoded_img.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    setitem(decoded_img, outfile)


def encode_text(cover_path, outfile, secret_message):
    cover = getitem(cover_path)
    red_cover = cover.split()[0]
    green_cover = cover.split()[1]
    blue_cover = cover.split()[2]

    x_size = cover.size[0]
    y_size = cover.size[1]

    img_text = create_text_image(secret_message, cover.size)
    bw_encode = img_text.convert('1')

    encoded_img = Image.new("RGB", (x_size, y_size))
    pixels = encoded_img.load()
    for i in range(x_size):
        for j in range(y_size):
            red_cover_pix = bin(red_cover.getpixel((i, j)))
            old_pix = red_cover.getpixel((i, j))
            tencode_pix = bin(bw_encode.getpixel((i, j)))

            if tencode_pix[-1] == '1':
                red_cover_pix = red_cover_pix[:-1] + '1'
            else:
                red_cover_pix = red_cover_pix[:-1] + '0'
            pixels[i, j] = (int(red_cover_pix, 2), green_cover.getpixel((i, j)), blue_cover.getpixel((i, j)))

    setitem(encoded_img, outfile)


def usage():
    print('''
                Usage and Requirements
Encoding Usage : python lsb_steg.py -e < cover_img > < outfile > < secret_message >
Decoding Usage : python lsb_steg.py -d < steg_img > < outfile >
For help       : python lsb_steg.py -h or python lsb_steg.py --help

    *** make sure to add the extension for the outfile except the jpg(jpeg) format.

 > Embed a secret message into a cover image using LSB
Positional Arguments ->
    cover_img       :    path to cover image
    outfile         :    path to output file
    secret_message  :    Enter your message that needs to be hidden

 > Extract a secret from a steganographic image using LSB on the red channel
 Positional Arguments ->
    steg_img        :    path of the steg image
    outfile         :    path to the output file

A basic Python 3 Script
Dependencies ->
    sudo apt-get install python3-pip
    sudo pip3 install Pillow
        -> ( Pillow or PIL )    
    sudo pip3 install textwrap
        -> if textwrap is not available''')


def main():
    if sys.argv[1] == '-e' and len(sys.argv) > 4:
        cover_img = sys.argv[2]
        outfile = sys.argv[3]
        secret_message = sys.argv[4:]
        secret_message = ' '.join(secret_message)
        encode_text(cover_img, outfile, secret_message)
    elif len(sys.argv) == 4 and sys.argv[1] == '-d':
        steg_img = sys.argv[2]
        outfile = sys.argv[3]
        decode_text(steg_img, outfile)
    elif (sys.argv[1] == '-h' or '--help') and len(sys.argv) < 3:
        usage()
    else:
        print(sys.argv)
        print("[ ! ] lsb_steg.py error : {} \nInvalid command !!! Try '-h' or '--help' ".format(sys.argv[3:]))


if __name__ == '__main__':
    main()
