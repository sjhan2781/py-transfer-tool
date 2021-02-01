from checker.none_checker import NoneChecker


class SchoolStatus:

    def __init__(self, num, name, status, inside, outside, gone, term, area):
        self.num = num
        self.name = name
        # self.status = status.value
        self.status = NoneChecker.check_valid(self, status)
        self.inside = NoneChecker.check_valid(self, inside)
        self.outside = NoneChecker.check_valid(self, outside)
        self.gone = NoneChecker.check_valid(self, gone)
        self.term = NoneChecker.check_valid(self, term)
        self.area = area

    def __str__(self) -> str:
        return '순={} 학교명={} 구역={} 과부족={} 관내={} 관외={} 전출={} 기간제={}'\
            .format(self.num, self.name, self.area, self.get_state(), self.inside, self.outside, self.gone, self.term)

    def get_state(self):
        return self.status + self.inside + self.outside - self.gone + self.term

