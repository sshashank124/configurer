from colorsys import hls_to_rgb as hls_rgb

def hls_float(h, l , s):
    return (h / 360, l / 100, s / 100)

def hls_hex(h, l, s):
    return ''.join('%02x' % round(i * 255) for i in hls_rgb(*hls_float(h, l, s)))

def color_gradient_for(h, s, start, count):
    step_size = (100 - 2 * start) / (count - 1)
    return [hls_hex(h, start + int(i * step_size), s) for i in range(count)]
