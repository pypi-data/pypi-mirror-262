
class IMGTAnnotation:
    insertions = ["111.1", "111.2", "111.3", "111.4", "111.5", "111.6","111.7","111.8","112.9", "112.8", "112.7", "112.6", "112.5", "112.4", "112.3", "112.2", "112.1", "112", "113", "114", "115", "116", "117"]
    cdr3_labels = {
        3: [str(i) for i in list(range(105, 108))],
        4: [str(i) for i in list(range(105, 108))] + insertions[-1:],
        5: [str(i) for i in list(range(105, 108))] + insertions[-2:],
        6: [str(i) for i in list(range(105, 108))] + insertions[-3:],
        7: [str(i) for i in list(range(105, 109))] + insertions[-3:],
        8: [str(i) for i in list(range(105, 109))] + insertions[-4:],
        9: [str(i) for i in list(range(105, 110))] + insertions[-4:],
        10: [str(i) for i in list(range(105, 110))] + insertions[-5:],
        11: [str(i) for i in list(range(105, 111))] + insertions[-5:],
        12: [str(i) for i in list(range(105, 111))] + insertions[-6:],
        13: [str(i) for i in list(range(105, 112))] + insertions[-6:],
        14: [str(i) for i in list(range(105, 112))] + insertions[-7:],
        15: [str(i) for i in list(range(105, 112))] + insertions[:1]+ insertions[-7:],
        16: [str(i) for i in list(range(105, 112))] + insertions[:1]+ insertions[-8:],
        17: [str(i) for i in list(range(105, 112))] + insertions[:2]+ insertions[-8:],
        18: [str(i) for i in list(range(105, 112))] + insertions[:2]+ insertions[-9:],
        19: [str(i) for i in list(range(105, 112))] + insertions[:3]+ insertions[-9:],
        20: [str(i) for i in list(range(105, 112))] + insertions[:3]+ insertions[-10:],
        21: [str(i) for i in list(range(105, 112))] + insertions[:4] + insertions[-10:],
        22: [str(i) for i in list(range(105, 112))] + insertions[:4]+ insertions[-11:],
        23: [str(i) for i in list(range(105, 112))] + insertions[:5]+ insertions[-11:],
        24: [str(i) for i in list(range(105, 112))] + insertions[:5]+ insertions[-12:],
        25: [str(i) for i in list(range(105, 112))] + insertions[:6]+ insertions[-12:],
        26: [str(i) for i in list(range(105, 112))] + insertions[:6]+ insertions[-13:],
        27: [str(i) for i in list(range(105, 112))] + insertions[:7]+ insertions[-13:],
        28: [str(i) for i in list(range(105, 112))] + insertions[:7]+ insertions[-14:],
        29: [str(i) for i in list(range(105, 112))] + insertions[:8]+ insertions[-14:],
        30: [str(i) for i in list(range(105, 112))] + insertions[:8]+ insertions[-15:],
    }
    
    @staticmethod
    def fr1(length):
        return [str(i) for i in list(range(1, length + 1))]

    @staticmethod
    def cdr1(length):
        return [str(i) for i in list(range(27, 27 + length))]
    
    @staticmethod
    def fr2(length):
        
        return [str(i) for i in list(range(39, 39 + length))]
    
    @staticmethod
    def cdr2(length):
        return [str(i) for i in list(range(56, 56 + length))]
    
    @staticmethod
    def fr3(length):
        return [str(i) for i in list(range(66, 66 + length))]

    @staticmethod
    def cdr3(length, cdr3_labels = cdr3_labels):
        return cdr3_labels[length]
    
    @staticmethod
    def fr4(length):
        return [str(i) for i in list(range(118, 118 + length))]