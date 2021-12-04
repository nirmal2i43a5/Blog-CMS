from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
        # Starts signals to create author profile.
    def ready(self):
        from apps.blog import signals

