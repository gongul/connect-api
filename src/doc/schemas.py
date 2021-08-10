from drf_spectacular.openapi import AutoSchema

from common.errors import ErrorCollection

bad_request_response = ErrorCollection(target='field_name', message='잘못된 요청입니다.', code='invalid')
unauthorized_response = ErrorCollection(target='non_field', message='잘못된 인증 자격 증명입니다.', code='authentication_failed')
forbidden_response = ErrorCollection(target='non_field', message='접근 권한이 없습니다.', code='permission_denied')
not_found_response = ErrorCollection(target='non_field', message='리소스를 찾을 수 없습니다.', code='not_found')
method_not_allowed_response = ErrorCollection(target='non_field', message='해당 메소드는 허용되지 않습니다.', code='method_not_allowed')
server_error_response = ErrorCollection(target='non_field', message='알 수 없는 에러입니다.', code='server_error')

bad_request_response_sample = bad_request_response.to_schema(description='잘못된 요청을 했을 때 발생하는 에러 케이스 샘플입니다.',
                                                             code_enum=('parse_error', 'invalid', 'invalid_choice',
                                                                        'unique', 'required', 'blank', 'max_length', 'min_length'),
                                                             target_enum=('non_field', 'field_name'),
                                                             status_code=400)
unauthorized_response_sample = unauthorized_response.to_schema(description='인증 실패시 에러 케이스 샘플입니다.',
                                                               code_enum=('not_authenticated', 'authentication_failed'),
                                                               status_code=401)
forbidden_response_sample = forbidden_response.to_schema(description='접근 권한이 없을 때 에러 케이스 샘플입니다.',
                                                         status_code=403)
not_found_response_sample = not_found_response.to_schema(description='리소스가 없을 때 에러 케이스 샘플입니다.',
                                                         status_code=404)
method_not_allowed_response_sample = method_not_allowed_response.to_schema(description='API에서 해당 메소드를 허용하지 않을 때 에러 케이스 샘플입니다.',
                                                                           status_code=405)
server_error_response_sample = server_error_response.to_schema('서버에서 처리하지 못한 에러 케이스 샘플입니다.')


class CustomSchema(AutoSchema):
    def get_operation(self, path, path_regex, method, registry):
        operation = super().get_operation(path, path_regex, method, registry)

        if operation['responses'].get('400') is None:
            operation['responses']['400'] = bad_request_response_sample
        if operation['responses'].get('401') is None:
            operation['responses']['401'] = unauthorized_response_sample
        if operation['responses'].get('403') is None:
            operation['responses']['403'] = forbidden_response_sample
        if operation['responses'].get('404') is None:
            operation['responses']['404'] = not_found_response_sample
        if operation['responses'].get('405') is None:
            operation['responses']['405'] = method_not_allowed_response_sample
        if operation['responses'].get('500') is None:
            operation['responses']['500'] = server_error_response_sample

        operation['responses']

        return operation

    def get_description(self):
        ''' 내부 주석을 위해 class,method description을 제거 '''
        return None
