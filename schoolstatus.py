from none_checker import NoneChecker


class SchoolStatus:

    def __init__(self, num, name, status, inside, outside, gone, term):
        self.num = num.internal_value
        self.name = name.value
        # self.status = status.value
        self.status = NoneChecker.check_valid(self, status.value)
        self.inside = NoneChecker.check_valid(self, inside.value)
        self.outside = NoneChecker.check_valid(self, outside.value)
        self.gone = NoneChecker.check_valid(self, gone.value)
        self.term = NoneChecker.check_valid(self, term.value)

    def __str__(self) -> str:
        return '순={} 학교명={} 과부족={} 관내={} 관외={} 전출={} 기간제={}'\
            .format(self.num, self.name, self.get_state(), self.inside, self.outside, self.gone, self.term)

    def get_state(self):
        return self.status + self.inside + self.outside - self.gone + self.term
