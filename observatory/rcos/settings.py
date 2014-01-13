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
