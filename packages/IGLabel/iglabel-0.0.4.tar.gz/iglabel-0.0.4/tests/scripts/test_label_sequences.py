from src.iglabel.scripts.label_sequences import Label


def test_label_sequences():
    sequence = "CNANSYCSESVCYENPWYDYW"
    label = Label([sequence], ["CDR3"])
    position_dict, label_dict = label.get_imgt_label_ig()
    assert len(list(label_dict.values())[0]) == len(sequence)
    label = list(label_dict.values())[0]
    assert label == ["105", "106", "107", "108", "109", "110", "111", "111.1", "111.2", "111.3", "111.4", "112.4", "112.3", "112.2", "112.1", "112", "113", "114", "115", "116", "117"]
    sequence = "CNANSYCSE"
    label = Label([sequence], ["CDR3"])
    position_dict, label_dict = label.get_imgt_label_ig()
    assert len(list(label_dict.values())[0]) == len(sequence)
    label = list(label_dict.values())[0]
    assert label == ["105", "106", "107", "108", "109", "114", "115", "116", "117"]
    sequence = "CNANSYCSESVCY"
    label = Label([sequence], ["CDR3"])
    position_dict, label_dict = label.get_imgt_label_ig()
    assert len(list(label_dict.values())[0]) == len(sequence)
    label = list(label_dict.values())[0]
    assert label == ["105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117"]
    assert isinstance(position_dict,dict) == True, "The position_dict is not a dictionary"
