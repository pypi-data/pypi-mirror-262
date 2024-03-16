import os

class ShowBelongings:
    def __init__(self, igl:list, igl_seq:list,aminoacid_list:list, filename = "output.txt"):
        self.igl = igl
        self.igl_seq = igl_seq
        self.aminoacid_list = aminoacid_list   
        self.filename = self.check_filename(filename)
    @staticmethod
    def check_filename(filename):
        i = 1
        dir = os.path.dirname(filename)
        if os.path.exists(filename):
            while True:
                if os.path.exists(os.path.join(dir, f"{filename}({i}).txt")):
                    i += 1
                else:
                    base = os.path.basename(filename).strip(".txt")
                    filename = os.path.join(dir, base + f"({i}).txt")
                    break
        else:
            pass
        return filename
            

    def __call__(self):
        with open(self.filename, 'w') as f:
            for seq in range(len(self.igl_seq)):
            # Write values from the first list in the same row
                for val1 in self.igl_seq[seq]:
                    f.write(f'{val1:<8}')  # Use string formatting to align the values
                f.write('\n')  # Write a newline character to move to the next row

                # Write values from the second list in the same row
                for val2 in self.igl[seq]:
                    f.write(f'{val2:<8}')
                
                f.write('\n') 
                for val3 in self.aminoacid_list[seq]:
                    f.write(f'{val3:<8}')
                    
                f.write('\n\n\n')  # Write a newline character to move to the next row