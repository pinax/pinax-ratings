import pkg_resources

__version__ = pkg_resources.get_distribution("pinax-ratings").version
default_app_config = "pinax.ratings.apps.AppConfig"
