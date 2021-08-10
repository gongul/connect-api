from django.core.files.uploadedfile import UploadedFile
from django.conf import settings

import magic

ALLOW_MINE_TYPE = ['image/jpeg', 'image/jpg', 'image/png']


def validate_image(image):
    ''' 이미지 업로드 하기전에 공동으로 검증 해야하는 내용들 묶음
        self.is_allow_max_size
        self.is_allow_mime_type

    Args:
        images (UploadedFile): 검증할 이미지

    Returns:
        bool: 이미지에 문제가 없을 경우 True를 반환
    '''
    is_valid = False

    if isinstance(image, UploadedFile):
        is_max_size = _max_size_validate(image)
        is_mime_type = _mime_type_validate(image)

        if is_max_size and is_mime_type:
            is_valid = True

    return is_valid


def is_allow_max_size(image):
    '''이미지들을 가져와 max size 검증한다.

    Args:
        images (UploadedFile): 검증할 이미지들

    Returns:
        bool: 안전한 max size를 안넘으면 True 아니면 False
    '''
    is_allow: bool = False

    if isinstance(image, UploadedFile):
        is_allow = _max_size_validate(image)

    return is_allow


def is_allow_mime_type(image):
    '''이미지들을 가져와 mime-type 검증한다.

    Args:
        images (UploadedFile): 검증할 이미지들

    Returns:
        bool: 안전한 mime-type이면 True 아니면 False
    '''
    is_allow: bool = False

    if isinstance(image, UploadedFile):
        is_allow = _mime_type_validate(image)

    return is_allow


def _max_size_validate(image):
    if image.size > settings.FILE_UPLOAD_MAX_SIZE:
        return False

    return True


def _mime_type_validate(image):
    image.open()
    mine_type = magic.from_buffer(image.file.read(1024), mime=True)

    if mine_type not in ALLOW_MINE_TYPE:
        return False

    return True
