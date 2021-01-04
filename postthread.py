from PyQt5 import QtCore


class PostingThread(QtCore.QThread):
    go_to_next = QtCore.pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__()
        self.internal = kwargs['internal']
        self.external = kwargs['external']
        self.schools = kwargs['schools']
        self.hash_schools = kwargs['hash_schools']
        self.invited = kwargs['invited']
        self.priority = kwargs['priority']
        self.gone_external = kwargs['gone_external']

    def run(self) -> None:
        self.post()

    def post(self):
        self.before_post()
        self.post_invited()
        self.go_to_next.emit()

    def before_post(self):
        print('internal {} school {} external {}'
                    .format(self.internal.__len__(), self.schools.__len__(), self.external.__len__()))

        for teacher in self.invited:
            if teacher.disposed is not None:
                teacher.disposed = self.schools[self.hash_schools.get(teacher.disposed)-1]
            else:
                if '만기' in teacher.type or '비정기' in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone += 1

        for teacher in self.priority:
            if teacher.disposed is not None:
                teacher.disposed = self.schools[self.hash_schools.get(teacher.disposed)-1]
            else:
                if '만기' in teacher.type or '비정기' in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone += 1

        for teacher in self.internal:
            if teacher.disposed is not None:
                teacher.disposed = self.schools[self.hash_schools.get(teacher.disposed)-1]
            else:
                if '만기' in teacher.type or '비정기' in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone += 1

        for teacher in self.external:
            if teacher.disposed is not None:
                teacher.disposed = self.schools[self.hash_schools.get(teacher.disposed)-1]

    def post_invited(self):
        self.post_by_first(self.invited)
        self.post_priority()

    def post_priority(self):
        self.post_by_first(self.priority)
        self.post_by_first(self.internal)

    def post_by_first(self, teachers):
        for teacher in teachers:
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
                    self.post_invited()
                    return

        self.post_by_second(teachers)

    def post_by_second(self, teachers):
        for teacher in teachers:
            if teacher.disposed is not None:
                continue

            if teacher.second is not None:
                desired_school_num = self.hash_schools.get(teacher.second) - 1

                if self.schools[desired_school_num].get_state() < 0:
                    teacher.disposed = self.schools[desired_school_num]
                    self.schools[desired_school_num].inside += 1

                    self.post_invited()
                    return

        self.post_by_third(teachers)

    def post_by_third(self, teachers):
        for teacher in teachers:
            if teacher.disposed is not None:
                continue

            if teacher.third is not None:
                desired_school_num = self.hash_schools.get(teacher.third) - 1

                if self.schools[ desired_school_num].get_state() < 0:
                    teacher.disposed = self.schools[desired_school_num]
                    self.schools[desired_school_num].inside += 1

                    self.post_invited()
                    return

        # self.post_by_second(teachers)

