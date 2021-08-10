refresh_response_schema = {'type': 'object', 'properties': {
    'access_token': {'title': '엑세스 토큰', 'type': 'string'}
}}


obtain_response_schema = {'type': 'object', 'properties': {
    'access_token': {'title': '엑세스 토큰', 'type': 'string'},
    'refresh_token': {'title': '리프레쉬 토큰', 'type': 'string'}
}}
