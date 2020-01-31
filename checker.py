from abc import * # Abstrace Base Class


class Checker(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod # Character 클래스를 상속받는 모든 클래스는 하기 함수를 오버라이딩으로 구현해야 인스턴스 생성이 가능하다.
    def check_valid(self):
        pass
