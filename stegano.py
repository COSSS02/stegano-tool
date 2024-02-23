from PIL import Image
from argparse import ArgumentParser
import os.path


def encode_string(image, message, output_file):
    init_im = Image.open(image)
    if init_im.mode == 'RGBA':
        im = init_im.convert('RGB')
    else:
        im = init_im

    pixels = list(im.getdata())

    # length of the message in binary format, represented on 18 bits
    length_bin = list(format(len(message), '018b'))

    # the first 6 pixels from the image, required to have access to 18 bits
    length_pixels = [item for temp in pixels[0:6] for item in temp]

    # encodes the length of the message inside the first 6 pixels
    length_result = [length_pixels[index] & 0xFE | (ord(length_bin[index]) % 2)
                     for index in range(len(length_bin))]

    # modifies the original pixels
    it = iter(length_result[0:9])
    pixels[0:3] = list(zip(it, it, it))

    it = iter(length_result[9:])
    pixels[3:6] = list(zip(it, it, it))

    for i in range(len(message)):
        # letter from the message, represented on 9 bits
        bin_letter = list(format(ord(message[i]), '09b'))

        # the 3 pixels where the letter will be encoded
        current_pixels = [item for temp in pixels[i * 3 + 6:i * 3 + 9]
                          for item in temp]

        # encoding the letter inside the pixels
        result = [current_pixels[index] & 0xFE | (ord(bin_letter[index]) % 2)
                  for index in range(len(bin_letter))]

        # modifying the original pixels
        it = iter(result)
        pixels[i * 3 + 6:i * 3 + 9] = list(zip(it, it, it))

    new_im = Image.new(im.mode, im.size)
    new_im.putdata(pixels)

    if init_im.mode == 'RGBA':
        new_im = new_im.convert('RGBA')
        new_im.putalpha(init_im.split()[3])

    new_im.save(output_file)


def decode_string(image, output_file):
    init_im = Image.open(image)
    if init_im.mode == 'RGBA':
        im = init_im.convert('RGB')
    else:
        im = init_im

    pixels = list(im.getdata())

    # the pixels where the length of the message is stored
    length_pixels = [item for temp in pixels[0:6] for item in temp]

    # constructs the length's string in binary format
    string = ""
    for i in range(len(length_pixels)):
        if length_pixels[i] % 2:
            string += '1'
        else:
            string += '0'

    # converts the length to int
    length = int(string, 2)

    decoded_message = ""

    # decodes every letter from the message, taking 3 pixels at a time
    for i in range(length):
        current_pixels = [item for temp in pixels[i * 3 + 6:i * 3 + 9]
                          for item in temp]

        string = ""
        for j in range(len(current_pixels)):
            if current_pixels[j] % 2:
                string += '1'
            else:
                string += '0'

        decoded_message += chr((int(string, 2)))

    with open(output_file, "w") as f:
        print(decoded_message, file=f)


if __name__ == "__main__":
    parser = ArgumentParser(description='Steganography Tool')

    parser.add_argument('-e', '--encode',
                        help='Path to existing PNG image to encode message into')
    parser.add_argument('-d', '--decode',
                        help='Path to existing PNG image to decode message from')
    parser.add_argument('-m', '--message',
                        help='Message to be encrypted in output image')
    parser.add_argument('-o', '--output',
                        help='Path to output file(PNG image for encoding '
                             'or text file for decoding)')

    args = parser.parse_args()

    if not (args.encode or args.decode):
        parser.error('No action requested, add --encode or --decode')

    if args.encode:
        if not os.path.exists(args.encode):
            parser.error('The PNG image for encoding could not be found')

        if not args.encode.lower().endswith('.png'):
            parser.error('The file for encoding is not a PNG image')

        if not args.message:
            parser.error('No message to encode, add --message')

        if not args.output:
            parser.error('No PNG image for encoding, add --output')

        encode_string(args.encode, args.message, args.output)

    if args.decode:
        if not os.path.exists(args.decode):
            parser.error('The PNG image for decoding could not be found')

        if not args.decode.lower().endswith('.png'):
            parser.error('The file for decoding is not a PNG image')

        if not args.output:
            parser.error('No text file for the decoded message, add --output')

        decode_string(args.decode, args.output)