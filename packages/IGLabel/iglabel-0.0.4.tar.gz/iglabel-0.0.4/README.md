# IGLabel

This package provides and easy way to label your IG and T-cell receptor sequences according to the IMGT standard. 

## Installation

```r
pip install iglabel
```

## Usage



```python
import iglabel

label_dict, position_dict = IMGT(["CASSLGTGELFF"], ["CDR3"])
```
**INPUTS**
- sequences: A list of sequences for which you want to obtain the IMGT labels.
- regions: A list of regions in the same order as the sequences to receive the right labelling. Possible regions are: FR1, CDR1, FR2, CDR2, FR3, CDR3, FR4.

**RETURN**


- label_dict: Contains the sequences per region as keys and the corresponding IMGT labels as values.

- position_dict: Contains the IMGT labels as keys and the positions from n-lengthsequence as values.

- A [txt document](output.txt) which visualizes the sequence with the corresponding IMGT label.

#### *Example: Multiple Sequences*

You can parse multiple sequences at once if you want:

```python
label_dict, position_dict = IMGT(["CASSLGTG", "CASSLGTGELFF"], ["CDR2", "CDR3"])
``` 



## Citation

If you use this package, please cite the following paper:

```bibtex
Lefranc MP, Pommié C, Ruiz M, Giudicelli V, Foulquier E, Truong L, Thouvenin-Contet V, Lefranc G. IMGT unique numbering for immunoglobulin and T cell receptor variable domains and Ig superfamily V-like domains. Dev Comp Immunol. 2003 Jan;27(1):55-77. doi: 10.1016/s0145-305x(02)00039-3. PMID: 12477501.
```
