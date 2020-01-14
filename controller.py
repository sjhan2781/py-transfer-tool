import os

from PyQt5.QtCore import QObject
from openpyxl import load_workbook

from loadingwidget import LoadingWidget
from postthread import PostingThread
from schoolstatus import SchoolStatus
from start_view import StartView
from tableWidget import WorkingField
from teacher_external import TeacherExternal
from teacher_internal import TeacherInternal


class StartController(QObject):

    def __init__(self) -> None:
        super().__init__()

        self.loading = LoadingWidget(**{'controller': self,
                                        'title': '기다려주세요..',
                                        'internal': self.internal_list,
                                        'school': self.school_list,
                                        'external': self.external_list,
                                        'invited': self.invited_list})

        self.internal_list = list()
        self.school_list = list()
        self.external_list = list()
        self.invited_list = list()
        self.priority_list = list()
        self.hash_schools = dict()

        self.post_thread = PostingThread(internal=self.internal_list,
                                         external=self.external_list,
                                         schools=self.school_list,
                                         hash_schools=self.hash_schools,
                                         invited=self.invited_list,
                                         priority=self.priority_list)

        self.flag_internal = False
        self.flag_schools = False
        self.flag_external = False

    def get_internal_list(self, file_url):
        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['초등(학교별)']

            i = 0

            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                                    name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[22], first=row[24], second=row[25], third=row[26],
                                    date=row[8], remarks=row[27])

                if '우대' in t.type:
                    self.priority_list.append(t)
                else:
                    self.internal_list.append(t)
                i += 1

            ws = wb['초빙']

            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3], name=row[4],
                                    sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[22],
                                    first=row[24], second=row[25], third=row[26], date=row[8], remarks=row[27])

                self.invited_list.append(t)
                i += 1

            ws = wb['비정기']

            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3], name=row[4],
                                    sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[22],
                                    first=row[24], second=row[25], third=row[26], date=row[8], remarks=row[27])

                self.internal_list.append(t)
                i += 1

            self.internal_list.sort()

            wb.close()

        # except KeyError as e:
        #     show_msg_box("올바른 파일을 선택해주세요.", True)
        #     self.flag_internal = False

        except Exception as e:
            print(type(e))
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_internal = False

        else:
            self.flag_internal = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

    def get_school_list(self, file_url):
        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['결충원']

            for row in ws.iter_rows(min_row=8):
                if row[0].value is None:
                    break

                # print('{}'.format(row[51].internal_value))
                self.school_list.append(SchoolStatus(row[0], row[2], row[51]))
                self.hash_schools[row[2].value] = row[0].internal_value
            wb.close()

            # except KeyError as e:
            #     show_msg_box("올바른 파일을 선택해주세요.", True)
            #     self.flag_schools = False

        except Exception as e:
            print(type(e))
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_schools = False

        else:
            self.flag_schools = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

    def get_external_list(self, file_url):
        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(filename=file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['배정전정리']

            i = 0

            for row in ws.iter_rows(min_row=4):
                if row[0].value is None:
                    break

                t = TeacherExternal(i, row[0], '타시군전입', row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                    row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17],
                                    row[18], row[19], row[21], row[22], row[23])

                self.external_list.append(t)
                i += 1

            wb.close()

        # except KeyError as e:
        #     StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
        #     self.flag_external = False

        except Exception as e:
            print(e)
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_external = False

        else:
            self.flag_external = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

    def is_valid(self):

        if self.flag_internal and self.flag_external and self.flag_schools:
            return True

        else:
            msg = '불러오지 않은 파일이 있습니다.\n'

            if not self.flag_schools:
                msg += '결충원 현황'

            if not self.flag_internal:
                if msg:
                    msg += ', '
                msg += '순위명부'

            if not self.flag_external:
                if msg:
                    msg += ', '
                msg += '타시군 전입명부'

            StartView.show_msg_box(msg=msg, is_error=True)

            return False

    def start(self):
        self.loading.start()

    def show_next_view(self):
        print('internal {} school {} external {}'
              .format(self.internal_list.__len__(), self.school_list.__len__(), self.external_list.__len__()))
        field = WorkingField(internal=self.internal_list,
                             external=self.external_list,
                             schools=self.school_list,
                             invited=self.invited_list,
                             priority=self.priority_list)
