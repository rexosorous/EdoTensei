class Ninja:
    def __init__(self, name: str, image_dir: str, exp: int, BL_name: str, BL_exp: int):
        self.name = name
        self.image_dir = image_dir
        self.exp_start = exp
        self.exp = exp
        self.BL_name = BL_name
        self.BL_exp_start = BL_exp
        self.BL_exp = BL_exp