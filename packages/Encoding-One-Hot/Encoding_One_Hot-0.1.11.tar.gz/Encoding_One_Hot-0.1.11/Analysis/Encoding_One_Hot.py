import pandas as pd

class Encoding_One_Hot:
    
    def __init__(self) -> None:
        self.data = ...
        self.encoded = ...

    def set_target_attrib(self, df, attribute: str) -> ...:
        self.data = df[attribute]
        return self
        
    def encode(self) -> ...:
        x_axis = sorted(list(set(self.data)))
        self.encoded = {
            # Using this dictionary comprehension we can get the encoded value
            key: [1 if encode == x_axis[i] else 0 for encode in self.data] 
            for i, key in enumerate(x_axis)
        }
        return self
    
    def encoded_show(self):
        encoded_df = pd.DataFrame(self.encoded)
        encoded_df.set_index(self.data)
        encoded_df
        return encoded_df