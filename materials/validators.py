from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    """
    Валидатор для проверки, что ссылка ведет на youtube.com.
    """
    if "youtube.com" not in value:
        raise ValidationError("Ссылка должна вести на youtube.com")
