import magic
from django.core.exceptions import ValidationError

def validate_video(value):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(value.read(1024))
    if not file_type.startswith('video/'):
        raise ValidationError('The uploaded file is not a video.')
    
def file_size(value):
    limit = 100000000
    if value.size > limit:
        raise ValidationError('The uploaded file is too large. Should not exceed 100mb.')