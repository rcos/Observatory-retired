# RCOS Specific Settings

SITE_TITLE = "Rensselaer Center for Open Source Software"

# Address for the website
SITE_ADDRESS = "http://rcos.rpi.edu"
ALLOWED_HOSTS = [
    "rcos.rpi.edu"
]

# Location of the url configuration file
ROOT_URLCONF = 'observatory.rcos.urls'

# The address where emails should be sent from
MAIL_SENDER = "no-reply@rpi.edu"


# The web address that observatory is hosted on
DOMAIN_NAME = "http://rcos.rpi.edu"

## Page header
HEADER_TEMPLATE = 'rcos/header.html'

## Favicon
FAVICON_PATH = '/site-media/rcos/favicon.ico'

# The title prepended to any RSS feeds
FEED_TITLE = "RCOS"

# Location of the footer template partial
FOOTER = "rcos/partials/footer.html"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql'
        'NAME': 'observatory',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'zaq12wsxcde34rfv',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with 
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


