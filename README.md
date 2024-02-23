# Steganography tool

## Description

This project implements a method for you to conceal a message inside any
RGB/RGBA PNG image, while also providing an easy way to decode any other message
that was hidden using the same algorithm, all in a simple web interface.

## Implementation

The encoding of the message into the image is done using the least signifiant
bit of every color channel from the pixels. That means 3 pixels provide 9 bits
which can be used to represent a single letter from the message. But before
encoding the actual message, the length of the message must be placed in the
first 6 pixels of the image. That makes the extraction of the message from the
encoded image a very simple process.

The flask application provides several endpoints. Three of them are used for
displaying the pages of the website. One of them is the homepage, while the
other two provide an interface for the encryption algorithms described earlier.
These two web pages also display the last encoded/decoded images. Then there
are the two endpoints which handle the actual request and return the encoded
image, or the decoded message. Also, two additional endpoints can be used to
display the last encoded image, or the last decoded message.


## Libraries used

The only third-party libraries used in this project are python's _pillow_
module and the _flask_ web framework.

## Installation

The project can be built from the Dockerfile using the following command:

```bash
docker build -t stegano-tool .
```

In order to start the server from the docker image on _localhost:8080_:

```bash
docker run -p 8080:80 -it stegano-tool
```

Alternatively, the functions used for encoding and decoding can be used
directly from the python scrypt:

```bash
python3 stegano.py [-e/-d] input_file [-m message] -o output_file
```
