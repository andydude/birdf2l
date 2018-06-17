
def ollid(posid):
    up, slot = posid.split('/')
    up = ''.join(sorted(list(up)))
    up = '{}{}{}{}{}{}{}{}'.format(
        up[0], up[4],
        up[1], up[5],
        up[2], up[6],
        up[3], up[7])
    return '/'.join([up, slot])
    
