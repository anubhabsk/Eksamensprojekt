def isInRange(x, offset, min, max):
    return (x - offset) < min and (x + offset) > max

def isInBounds(pos, offset, min, max):
    return isInRange(pos[0], offset[0], min[0], max[0]) and isInRange(pos[1], offset[1], min[1], max[1])