from PIL import Image, ImageDraw

def main(fname):
    img = Image.open(fname+'.png')
    rgb_im = img.convert('RGB')

    mapa = {
        (255 ,255,255) : '?', # blanco         - especial
        (254 ,255,252) : '?', # blanco         - especial

        (204 ,204,204) : ' ', # gris muy claro - aire
        (204 ,202,206) : ' ', # gris muy claro - aire
        (148 ,44,67)   : '`', # rosa oscuro    - aire sobre agua

        (12  ,122,123) : '=', # azul           - ventana

        (12  ,255,0)   : '^', # verde          - pasto

        (50  ,51,49)   : '_', # gris oscuro    - calle
        (100 ,102,99)  : '.', # gris claro     - acera
        (102 ,102,102) : '.', # gris claro     - piso

        (128 ,127,3)   : '%', # cafe           - mueble

        (129 ,0,0)     : '#', # ladrillo       - muro
        (111 ,13,19)   : '#', # ladrillo       - muro

        (105 ,136,151) : '|', # gris azulado   - reja

        (250 ,0,0)     : '+', # rojo           - puerta cerrada
        (254 ,56,111)  : '*', # rosa           - puerta abierta

        (52  ,74,43)   : 'T', # verde oscuro   - arbol
        (252 ,251,0)   : 'X', # amarillo       - escalera

        (70  ,41,78)   : '~', # azul oscuro    - dentro de agua

        (0   ,1,0)     : ',', # negro          - roca
        (0   ,0,0)     : ',', # negro          - roca
        }

    img = Image.open(fname+'.png')
    rgb_im = img.convert('RGB')

    with open(fname+'.lev', 'w') as f:
        for y in range(rgb_im.size[1]):
            for x in range(rgb_im.size[0]):
                char = mapa[rgb_im.getpixel((x,y))]
                f.write(char)
            f.write('\n')


def main_2(fname):
    img = Image.open(fname+'.png')
    rgb_im = img.convert('RGB')
    cols = set()
    for y in range(rgb_im.size[1]):
        for x in range(rgb_im.size[0]):
            cols.add(rgb_im.getpixel((x,y)))

    im = Image.new("RGB", (150,24*len(cols)))
    draw = ImageDraw.Draw(im)
    for n,c in enumerate(cols):
        draw.rectangle([(0, n*20), (30, n*20+5)], fill=c)
        draw.text((35, n*20), str(c), fill=(255,255,255))

    im.save("palete_{}.png".format(fname),"PNG")


if __name__=="__main__":
    import sys
    main(sys.argv[1])
