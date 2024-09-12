class Tag:
    def __init__(self, tag, count):
        self.tag = tag
        self.count = count

    def __repr__(self):
        return f"TagData(tag='{self.tag}', count={self.count})"
