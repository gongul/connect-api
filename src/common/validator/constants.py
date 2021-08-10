
class BaseValidationMessage():
    '''열거형 대신으로 사용하기 때문에 객체로 만들어서 사용하지 말것.'''
    required = ''
    max_length = ''
    min_length = ''
    blank = ''
    invalid = ''
    invalid_choice = ''
    unique = ''

    def __init__(self):
        raise SyntaxError('해당 클래스를 객체로 만들어서 사용하지 마세오.')

    @classmethod
    def to_dict(cls):
        '''클래스 변수들을 묶어서 dictionany 형식으로 바꿔서 리턴한다'''
        result = {}
        class_dict: dict = vars(cls)

        for key, value in class_dict.items():
            if key.find('__') != -1 or value == '':
                continue

            result[key] = value

        return result
