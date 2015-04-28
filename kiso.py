
def box_dx_dy(box, dx, dy):
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)

def inBox(p, box):
    return box[0] < p[0] and p[0] < box[2] and box[1] < p[1] and p[1] < box[3]

def get_pos_ld(box):
    return (box[0], box[1])

def getSurroundBox(box, dx):
    return (box[0] - dx, box[1] - dx, box[2] + dx, box[3] + dx)
