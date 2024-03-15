class AddonError(Exception):
    def __init__(self, error_text):
        self.error_text = error_text
        print(error_text)
