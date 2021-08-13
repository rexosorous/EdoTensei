class Ninja:
    def __init__(self, name: str, image_dir: str, exp: int, BL_name: str, BL_exp: int):
        self.name = name
        self.image_dir = image_dir
        self.ninja_exp_start = exp
        self.ninja_exp_curr = exp
        self.ninja_ex_gain = 0
        self.BL_name = BL_name
        self.BL_exp_start = BL_exp
        self.BL_exp_curr = BL_exp
        self.BL_exp_gain = 0

    def update_exp(self, ninja: int, BL: int):
        self.ninja_exp_curr = ninja
        self.BL_exp_curr = ninja

        self.ninja_exp_gain = self.ninja_exp_curr - self.ninja_exp_start
        self.BL_exp_gain = self.BL_exp_curr - self.BL_exp_start