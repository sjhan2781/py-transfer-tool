import os

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from openpyxl import load_workbook

from loadingwidget import LoadingWidget
from postthread import PostingThread
from savethread import SavingThread
from savingwidget import SavingWidget
from schoolstatus import SchoolStatus
from start_view import StartView
from tableWidget import WorkingField
from teacher_external import TeacherExternal
from teacher_internal import TeacherInternal


class StartController(QObject):

    def __init__(self) -> None:
        super().__init__()

        self.internal_list = list()
        self.school_list = list()
        self.external_list = list()
        self.invited_list = list()
        self.priority_list = list()
        self.hash_schools = dict()

        self.designation = list()
        self.gone = list()

        self.internal_file_url = None
        self.external_file_url = None
        self.school_file_url = None

        self.post_thread = PostingThread(internal=self.internal_list,
                                         external=self.external_list,
                                         schools=self.school_list,
                                         hash_schools=self.hash_schools,
                                         invited=self.invited_list,
                                         priority=self.priority_list)

        self.save_thread = SavingThread(internal=self.internal_list,
                                        external=self.external_list,
                                        schools=self.school_list,
                                        hash_schools=self.hash_schools,
                                        invited=self.invited_list,
                                        priority=self.priority_list,
                                        designation=self.designation,
                                        gone=self.gone,
                                        internal_file_url=self.internal_file_url,
                                        external_file_url=self.external_file_url,
                                        school_file_url=self.school_file_url,
                                        controller=self)

        self.loading_post = LoadingWidget(**{'controller': self,
                                             'title': '기다려주세요..',
                                             'internal': self.internal_list,
                                             'school': self.school_list,
                                             'external': self.external_list,
                                             'invited': self.invited_list})

        self.waiting_save = SavingWidget(**{'controller': self,
                                            'title': '저장중입니다..',
                                            'internal': self.internal_list,
                                            'school': self.school_list,
                                            'external': self.external_list,
                                            'invited': self.invited_list,
                                            'designation': self.designation,
                                            'gone': self.gone})

        self.init_thread()

        self.flag_internal = False
        self.flag_schools = False
        self.flag_external = False

    def init_thread(self):
        self.post_thread.started.connect(self.loading_post.show)
        self.post_thread.finished.connect(self.loading_post.close)
        self.post_thread.finished.connect(self.show_next_view)

        self.save_thread.show_msg_box.connect(self.show_msg_box)
        self.save_thread.finished.connect(self.waiting_save.close)

        self.save_thread.started.connect(self.waiting_save.show)
        self.save_thread.started.connect(self.waiting_save.set_maximum)
        self.save_thread.set_state_internal.connect(self.waiting_save.ui.progressBar_internal.setValue)
        self.save_thread.set_state_external.connect(self.waiting_save.ui.progressBar_external.setValue)
        self.save_thread.set_state_school.connect(self.waiting_save.ui.progressBar_school.setValue)
        self.save_thread.set_state_result.connect(self.waiting_save.ui.progressBar_result.setValue)

    def get_internal_list(self, file_url):
        self.internal_list.clear()
        self.invited_list.clear()
        self.internal_file_url = file_url

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
                                    transfer_score=row[30], first=row[24], second=row[25], third=row[26],
                                    date=row[8], remarks=row[27], disposed=row[31])

                if '우대' in t.type:
                    self.priority_list.append(t)
                else:
                    self.internal_list.append(t)
                i += 1

            i = 0
            ws = wb['초빙']
            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                                    name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[30], first=row[24], second=row[25], third=row[26],
                                    date=row[8], remarks=row[27], disposed=row[31])

                self.invited_list.append(t)
                i += 1

            ws = wb['비정기']
            i = 0
            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                                    name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[30], first=row[24], second=row[25], third=row[26],
                                    date=row[8], remarks=row[27], disposed=row[31])

                self.internal_list.append(t)
                i += 1

            self.internal_list.sort()

        except TypeError as e:
            print(e)
            print(t.id)
            self.show_msg_box("{}시트 {}번 행 서식을 확인해주세요.".format(ws.title, i+6), True)
            self.flag_internal = False

        except KeyError as e:
            print(e)
            self.show_msg_box("시트 이름을 확인해주세요.", True)
            self.flag_internal = False

        except Exception as e:
            print(e)
            self.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_internal = False

        else:
            self.flag_internal = True
            self.show_msg_box("성공적으로 불러왔습니다.", False)

        finally:
            wb.close()

    def get_school_list(self, file_url):
        self.school_list.clear()
        self.school_file_url = file_url
        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['결충원']

            i = 0
            for row in ws.iter_rows(min_row=8):
                if row[0].value is None:
                    break

                # print('{}'.format(row[51].internal_value))
                self.school_list.append(SchoolStatus(num=row[0], name=row[2], status=row[51],
                                                     outside=row[55], inside=row[53], gone=row[52], term=row[63]))
                self.hash_schools[row[2].value] = row[0].internal_value
                self.designation.append([])
                self.gone.append([])
                i += 1

        except TypeError as e:
            print(e)
            self.show_msg_box("{}번째 행 서식을 확인해주세요.".format(i + 8), True)
            self.flag_internal = False

        except KeyError as e:
            print(e)
            self.show_msg_box("시트 이름을 확인해주세요.".format(t.id + 1), True)
            self.flag_internal = False

        except Exception as e:
            print(e)
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_schools = False

        else:
            # self.designation = [[] for row in range(self.school_list.__len__())]
            # self.gone = [[] for row in range(self.school_list.__len__())]
            self.flag_schools = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

        finally:
            wb.close()

    def get_external_list(self, file_url):
        self.external_list.clear()
        self.external_file_url = file_url

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

                if '미지정' in row[4].value:
                    type = '미지정'
                else:
                    type = '타시군전입'

                t = TeacherExternal(id=i, rank=row[0], type=type, region=row[1], position=row[2], school=row[3],
                                    name=row[4], birth=row[5], sex=row[6], major=row[8], career=row[7],
                                    first=row[9], second=row[10], third=row[11], ab_type=row[12], ab_start=row[13],
                                    ab_end=row[14], related_school=row[15], relation=row[16], relation_person=row[17],
                                    address=row[18], phone=row[19], email=row[20], vehicle=row[21], remarks=row[22])

                self.external_list.append(t)
                i += 1

        except TypeError as e:
            print(e)
            self.show_msg_box("{}번째 행 서식을 확인해주세요.".format(i + 2), True)
            self.flag_internal = False

        except KeyError as e:
            print(e)
            self.show_msg_box("시트 이름을 확인해주세요.", True)
            self.flag_internal = False

        except Exception as e:
            print(e)
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_external = False

        else:
            self.flag_external = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

        finally:
            wb.close()

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

    def start_program(self):
        self.post_thread.start()

    def show_next_view(self):
        print('internal {} school {} external {}'
              .format(self.internal_list.__len__(), self.school_list.__len__(), self.external_list.__len__()))

        self.field = WorkingField(internal=self.internal_list,
                                  external=self.external_list,
                                  schools=self.school_list,
                                  invited=self.invited_list,
                                  hash_school=self.hash_schools,
                                  designation=self.designation,
                                  gone=self.gone,
                                  priority=self.priority_list,
                                  controller=self, )

    def save(self, file_url):
        self.save_thread.internal_file_url = self.internal_file_url
        self.save_thread.external_file_url = self.external_file_url
        self.save_thread.school_file_url = self.school_file_url
        self.save_thread.result_file_url = file_url
        self.save_thread.start()

    def show_msg_box(self, msg, is_error):
        msg_box = QMessageBox()

        if is_error:
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.NoIcon)

        msg_box.setText(msg)
        msg_box.setWindowTitle("")
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec()
