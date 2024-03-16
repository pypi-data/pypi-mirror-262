from ..lib.imgt_annotations import IMGTAnnotation

class Label:
    def __init__(self, sequence:list, region:list, system = "IG"):
        self.sequence = sequence
        self.region = [local.lower() for local in region]
        self.system = system
        self.check_input(self.sequence, self.region, self.system)
        
    @staticmethod
    def get_sequence_length(sequence):
        return len(sequence)
    
    @staticmethod
    def check_input(sequence,region,system):
        if not isinstance(sequence, list):
            raise ValueError("The sequence must be a list")
        if not isinstance(region, list):
            raise ValueError("The region must be an list")
        if not isinstance(system, str):
            raise ValueError("The system must be a string")
        if system not in ["IG", "TR"]:
            raise ValueError("The system must be either IG or TR")
        for local in region:
            if local not in ["fr1", "cdr1", "fr2", "cdr2", "fr3", "cdr3", "fr4"]:
                raise ValueError(f"The region must be either FR1, CDR1, FR2, CDR2, CDR3 or FR4. Your region is {local}")


    def get_imgt_label_ig(self):
        label_dict = {}
        position_dict = {}
        for local_region, sequence in zip(self.region, self.sequence):
            seq_length = self.get_sequence_length(sequence)
            if seq_length >= 30:
                return "The sequence is too long. The maximum length is 29.", 0
            labels = getattr(IMGTAnnotation, local_region)(seq_length)
            assert len(labels) == seq_length, f"The length of the sequence is {seq_length} and the length of the labels is {len(labels)}. They must be equal."
            label_dict[sequence] = labels
            position_dict[tuple(str(i) for i in list(range(1, seq_length + 1)))] = labels
            
        return position_dict, label_dict
            
