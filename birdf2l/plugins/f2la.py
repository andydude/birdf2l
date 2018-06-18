
def has_cross(pos):
    if pos.eo[8] != 0: return False
    if pos.eo[9] != 0: return False
    if pos.eo[10] != 0: return False
    if pos.eo[11] != 0: return False
    if pos.ep[8] != 8: return False
    if pos.ep[9] != 9: return False
    if pos.ep[10] != 10: return False
    if pos.ep[11] != 11: return False
    return True


def has_u_slot(pos):
    if pos.eo[4] != 0: return False
    if pos.ep[4] != 4: return False
    if pos.co[4] != 0: return False
    if pos.cp[4] != 4: return False
    return True

def has_v_slot(pos):
    if pos.eo[5] != 0: return False
    if pos.ep[5] != 5: return False
    if pos.co[5] != 0: return False
    if pos.cp[5] != 5: return False
    return True

def has_w_slot(pos):
    if pos.eo[6] != 0: return False
    if pos.ep[6] != 6: return False
    if pos.co[6] != 0: return False
    if pos.cp[6] != 6: return False
    return True

def has_x_slot(pos):
    if pos.eo[7] != 0: return False
    if pos.ep[7] != 7: return False
    if pos.co[7] != 0: return False
    if pos.cp[7] != 7: return False
    return True


def is_ll(pos):
    if not has_cross(pos): return False
    if not has_u_slot(pos): return False
    if not has_v_slot(pos): return False
    if not has_w_slot(pos): return False
    if not has_x_slot(pos): return False
    return True


def is_f2l(pos):
    if not has_cross(pos): return False
    if not has_u_slot(pos): return False
    if not has_w_slot(pos): return False
    if not has_x_slot(pos): return False
    return True
