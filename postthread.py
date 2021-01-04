from PyQt5 import QtCore


class PostingThread(QtCore.QThread):
    go_to_next = QtCore.pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__()
        self.internal = kwargs['internal']
        self.external = kwargs['external']
        self.schools = kwargs['schools']
        self.hash_schools = kwargs['hash_schools']

    def run(self) -> None:
        self.post()

    def post(self):
        self.before_post()
        self.post_by_first()
        self.go_to_next.emit()

    def before_post(self):
        print('internal {} school {} external {}'
                    .format(self.internal.__len__(), self.schools.__len__(), self.external.__len__()))

        # 관내 전출희망교사
        for teacher in self.internal:
            # 임지지정된 교사
            if teacher.disposed is not None:
                teacher.disposed = self.schools[self.hash_schools.get(teacher.disposed)-1]
            # 임지지정 되지 않은 교사
            else:
                # 만기나 비정기의 경우 무조건 나가야하기 때문에 미리 결원명단에 추가
                if '만기' in teacher.type or '비정기' in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone += 1

        # 관외 전입교사
        for teacher in self.external:
            if teacher.disposed is not None:
                teacher.disposed = self.schools[self.hash_schools.get(teacher.disposed)-1]

    def post_by_first(self):
        for teacher in self.internal:
            if teacher.disposed is not None:
                continue

            if teacher.first is not None:
                pre_school_num = self.hash_schools.get(teacher.school) - 1
                desired_school_num = self.hash_schools.get(teacher.first) - 1

                if self.schools[desired_school_num].get_state() < 0:
                    teacher.disposed = self.schools[desired_school_num]
                    self.schools[desired_school_num].inside += 1

                    if '일반' in teacher.type or '초빙' in teacher.type:
                        self.schools[pre_school_num].gone += 1

                    self.post_by_first()
                    return

        self.post_by_second()

    def post_by_second(self):
        for teacher in self.internal:
            if teacher.disposed is not None:
                continue

            if teacher.second is not None:
                desired_school_num = self.hash_schools.get(teacher.second) - 1

                if self.schools[desired_school_num].get_state() < 0:
                    teacher.disposed = self.schools[desired_school_num]
                    self.schools[desired_school_num].inside += 1
                    self.post_by_first()
                    return

        self.post_by_third()

    def post_by_third(self):
        for teacher in self.internal:
            if teacher.disposed is not None:
                continue

            if teacher.third is not None:
                desired_school_num = self.hash_schools.get(teacher.third) - 1

                if self.schools[ desired_school_num].get_state() < 0:
                    teacher.disposed = self.schools[desired_school_num]
                    self.schools[desired_school_num].inside += 1

                    self.post_by_first()
                    return

