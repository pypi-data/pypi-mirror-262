from src.iglabel.scripts.create_overview_seq import ShowBelongings
from src.iglabel.scripts.label_sequences import Label


def test_overview():
    sequence = "CNANSYCSESVCYENPWYDYW"
    label = Label([sequence], ["CDR3"])
    position_dict, label_dict = label.get_imgt_label_ig()
    base_pos = list(position_dict.keys())
    imgt_pos = list(position_dict.values())
    amino_acid_list = list(label_dict.keys())
    ShowBelongings(base_pos, imgt_pos, amino_acid_list)()
    sequence = "CNANSYCSESVCYENPWYDYW"
    sequencecdr2 = "CNANSYCSES"
    label = Label([sequencecdr2, sequence], ["CDR2", "CDR3"])
    position_dict, label_dict = label.get_imgt_label_ig()
    base_pos = list(position_dict.keys())
    imgt_pos = list(position_dict.values())
    amino_acid_list = list(label_dict.keys())
    ShowBelongings(base_pos, imgt_pos, amino_acid_list)()