class SchoolStatus:

    def __init__(self, num, name, status):
        self.num = num.internal_value
        self.name = name.value
        # self.status = status.value
        self.status = status.internal_value
        self.inside = 0
        self.outside = 0
        self.gone = 0

    def __str__(self) -> str:
        return '순={} 학교명={} 과부족={} 관내={} 관외={} 전출={}'\
            .format(self.num, self.name, self.get_state(), self.inside, self.outside, self.gone)

    def get_state(self):
        return self.status + self.inside + self.outside - self.gone
