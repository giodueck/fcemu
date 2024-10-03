import base64
import zlib

# 32x64-value cell ROM, for loading into 64-value cell RAM module
rom_bp_placeholder = lambda i: str(0x7F000000 - 0x80000000 + i)
rom_bp_capacity = 4096
rom_bp_label = '64-value ROM'
rom_bp_description = '64-value ROM with decimal(0xFF000000 + i) as a placeholder value for the ith word.\\n\\n4096 words. For programming with outside tools.'
rom_bp_string = '0eNrNvV2vJVeVrvlXLF91q3Fpju85kfqiv6o4nDoU7aa56VNCxk4g1cZppdNUoRL//UQaBMVeEStWzHhi780FkjNzj9wfK8cYK+bzzPc/Pv3119+/+fb9228+fPrj//j0qzffffn+7bcf3r775tMff5r+2R++WH77k8//5b998m9vP/zuk6/efPn29198/T+1f//Hf2w//O+T/+WTt//zJ19898kXn3z79Rdfvvndu6+/evP+kz9/3G/evf/kw+/efPLxQ//t3fuv/uG/f/Pfv/E28of/+u4fPvnH5Q98+/7db99/8fvfv/3mt3/+S959/+G7t1+9+eTDu3dff/cPn/7o07dfvvvmu09//P/9x6ffvf3tN198/fEz/fDHb98sn+If3r7/8P3yKz/69Jsvfv/xF/78Jz7LT/+0fNw3X735909/LH/60YGP9P/0kXroIz//Tx9phz7yX/7TR/qf/vVHn7755sPbD2/f/PmL/uE//virb77//a/fvF++nL9+9Mdvy4cvvvnw2Zfvfv/rt9988eHd+6X0t+++e/vnH+B/fPrxMyn5h/jRp3/89MefRfuHWP6i5cM+vH/39a9+/eZ3X/zh7fIxyx/8zduvP7x5f/Cb3D79odr3H187n0lWlUpOfttlpVZM/iB0pZZP/mhspZb9px/W4ZfWk1r611pxqFas1JK/1spDtXKlVvtrrTpUq25rtfHXWv1Qrb5Sq/+11jhUa6zUqr+9VtuhYv/bSrH/9MI/9sr/31eK/e2VL8de+v/HSrG/vfTl2Gv//1wp9rfXvhx78f9fK8X+9uKXY6/+f1wp9rdXv+Sf/vXPfe6bN19+bIXffSwpH//v/Zuv/nNPffvVx37wr3/608e//Umf1aN91s722bcf3vz+b1/qv71799XNlynddxrs3xf58t3ym7dFbKez/n2R7z68++bNShXd6al/X+Xt+3fffPbu/Voh2WmoT7+mb799836jVNvpp39f6vv3X3zz9vvfr9eqsdNP/77W+y/+7bPfvP3udyuF+k4zXflGLcvUh7XPqXZ66eq3aqtY7jTTJy+Dd1+//eqz33z/ZuUVVbHXS5++pN68+Xrz8/K9Xvr3xZYy3314++Vnv/7i/Uox2+ulTz6z77/+zfdrdXSvjf59nV9/8WH5l/7HlUKy10L/vtCbf//266XV/GHZBm9rtb0O+uT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'


def generate_bp(program: list[int]) -> str:
    length = rom_bp_capacity
    while len(program) < length:
        program.append(0)

    b64_string = rom_bp_string[1:]
    bin_string = base64.b64decode(bytes(b64_string, 'utf-8'))

    json = zlib.decompress(bin_string)

    # Add first comment starting with ;; as label in blueprint
    json = json.replace(bytes('"label":"' + rom_bp_label + '"', 'utf-8'), bytes('"label":"' + bp_label_str + '"', 'utf-8'), 1)

    # Add comments before valid keywords as description in blueprint
    json = json.replace(bytes('"description":"' + rom_bp_description + '"', 'utf-8'), bytes('"description":"' + bp_desc_str + '"', 'utf-8'), 1)

    t = str(json)[2:-1]

    for i in range(length):
        if type(rom_bp_placeholder) == str:
            t = t.replace(rom_bp_placeholder, str(program[i]), 1)
        else:
            t = t.replace(rom_bp_placeholder(i), str(program[i]), 1)

    z = zlib.compress(bytes(t, 'utf-8'), level=9)
    b = '0' + str(base64.b64encode(z))[2:-1]

    return b

program = []
for i in range(rom_bp_capacity):
    # program.append(0x7F000000 - 0x80000000 + i)
    program.append(i)

for i in range(10):
    print(f'{program[i]}')

for i in range(10, 0, -1):
    print(f'{program[-i]}')

bp_label_str = rom_bp_label
bp_desc_str = rom_bp_description

print(generate_bp(program))