# lsb_steganography
Python program based on least significant bit (LSB) steganography, one of the basic stegonographical methods to hide data inside an image.

## Usage

Embed a secret message into a cover image using LSB

> Encoding Usage : python lsb_steg.py -e < cover_img > < outfile > < secret_message > 

Positional Arguments ->

    cover_img       :    path to cover image
    
    outfile         :    path to output file
    
    secret_message  :    Enter your message that needs to be hidden
    

   *** make sure to add the extension for the outfile except the jpg(jpeg) format. ***
    

 Extract a secret from a steganographic image using LSB on the red channel
 
 > Decoding Usage : python lsb_steg.py -d < steg_img > < outfile > 
 
 Positional Arguments ->
 
    steg_img        :    path of the steg image
    
    outfile         :    path to the output file
    
> For help       : python lsb_steg.py -h or python lsb_steg.py --help 


## Dependencies ->
    sudo apt-get install python3-pip
    sudo pip3 install Pillow
        -> ( Pillow or PIL )    
    sudo pip3 install textwrap
        -> if textwrap is not available''')

