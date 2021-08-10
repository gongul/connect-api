class ErrorCollection(object):
    def __init__(self, target, message, code):
        self.code = code
        self.target = target
        self.message = message

    def to_schema(self, description=None, target_enum=None, code_enum=None, status_code=500):
        schema = {'content':
                  {'application/json':
                   {'schema': {'type': 'object', 'description': description, 'properties': {
                       'status_code': {'title': '에러 상태 코드', 'type': 'number', 'example': status_code},
                       'errors': {'title': '에러 리스트', 'type': 'array', 'items': {'title': '에러 상세 내용', 'type': 'object', 'properties': {
                           'target': {'title': '에러 발생 필드', 'type': 'string', 'example': self.target, 'enum': target_enum},
                           'message': {'title': '에러 메세지', 'type': 'string', 'example': self.message},
                           'code': {'title': '에러 코드', 'type': 'string', 'example': self.code, 'enum': code_enum}
                       }}}}}}}}

        return schema
