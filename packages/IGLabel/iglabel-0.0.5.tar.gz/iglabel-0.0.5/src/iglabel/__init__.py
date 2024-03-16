from .lib.citation import cite
print(cite)


from .scripts.create_overview_seq import ShowBelongings
from .scripts.label_sequences import Label
import json

def IMGT(sequences, regions, save=True):
    label = Label(sequences, regions)
    position_dict, label_dict = label.get_imgt_label_ig()
    base_pos = list(position_dict.keys())
    imgt_pos = list(position_dict.values())
    amino_acid_list = list(label_dict.keys())
    if save:
        ShowBelongings(base_pos, imgt_pos, amino_acid_list)()
        with open('imgt_labes', 'w') as f:
            json.dump(label_dict, f)
        
    return label_dict, position_dict




