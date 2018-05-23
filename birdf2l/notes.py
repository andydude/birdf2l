
def is_strict(alg, present, missing):
    for c in list(present):
        if c not in alg:
            return False
    for c in list(missing):
        if c in alg:
            return False
    return True

def is_ru(alg):
    if is_strict(alg, "RU", "BDFL"):
        return True
    elif is_strict(alg, "FU", "BDLR"):
        return True
    elif is_strict(alg, "LU", "BDFR"):
        return True
    elif is_strict(alg, "BU", "DFLR"):
        return True
    else:
        return False
    
def is_rfu(alg):
    if is_strict(alg, "FRU", "BDL"):
        return True
    elif is_strict(alg, "FLU", "BDR"):
        return True
    elif is_strict(alg, "BLU", "DFR"):
        return True
    elif is_strict(alg, "BRU", "DFL"):
        return True
    else:
        return False
    
def is_rfl(alg):
    if is_strict(alg, "FLR", "BDU"):
        return True
    elif is_strict(alg, "BFL", "DRU"):
        return True
    elif is_strict(alg, "BLR", "DFU"):
        return True
    elif is_strict(alg, "BFR", "DLU"):
        return True
    else:
        return False
    
def is_rul(alg):
    if is_strict(alg, "RUL", "BDF"):
        return True
    elif is_strict(alg, "FUB", "DLR"):
        return True
    else:
        return False
    
def notes(alg):
    if is_ru(alg):
        return "RU"
    elif is_rfu(alg):
        return "RFU"
    elif is_rfl(alg):
        return "RFL"
    elif is_rul(alg):
        return "RUL"
    else:
        return None
    
