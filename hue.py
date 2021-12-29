from PIL import Image
import numpy as np
import colorsys

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def colorize(image, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    img = image.convert('RGBA')
    arr = np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(shift_hue(arr, hue/360.).astype('uint8'), 'RGBA')

    return new_img
    
im = Image.open('lowpoly/output/tiger/0030.png')
#layer = Image.new('RGB', im.size, 'red') # "hue" selection is done by choosing a color...
#output = Image.blend(im, layer, 0.5)

for i in range(0, 100):
    output = colorize(im, i)
    output.save(f"lowpoly/output/tiger-hue/{i:04d}.png", 'PNG')