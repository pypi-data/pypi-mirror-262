def print_in_color(text, style=None, color_red=False, color_orange=False, color_green=False, updating=False):
    if color_red:
        color = f'255;0;0'
    elif color_orange:
        color = f'244;92;33'
    elif color_green:
        color = f'61;184;44'
    else:
        color = '255;255;255'

    def get_style(styles):
        if styles == None:
            return ''
        styles = list(styles)
        STYLES = {
            'b': 1,
            'f': 2,
            'i': 3,
            'u': 4,
            's': 9,
        }
        res = ''
        for style in styles:
            if style not in STYLES:
                return ''
            res += ';' + str(STYLES.get(style))
        return res

    style = get_style(style)
    if updating:
        updating_end = '\r'
    else:
        updating_end = None

    print(f"\x1B[38;2;{color}{style}m{text}\x1B[0m", end=updating_end)

if __name__ == '__main__':
    from time import sleep
    print_in_color('new text 1', color_red=True, updating=True)
    sleep(0.5)
    print_in_color('new text 2', color_red=True, updating=True)
    sleep(0.5)
    print_in_color('new text 3', color_red=True, updating=True)
    sleep(0.5)
    print_in_color('new text 4', color_green=True, style='bu')
