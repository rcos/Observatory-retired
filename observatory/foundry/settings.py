# Foundry Specific Settings

# Address for the website
SITE_ADDRESS = "http://www.edustartup.org/rpi"
ALLOWED_HOSTS = [
    "edustartup.org"
]

SITE_TITLE = 'RPI Foundry'
# Location of the url configuration file
ROOT_URLCONF = 'observatory.foundry.urls'

# The address where emails should be sent from
MAIL_SENDER = "no-reply@edustartup.org"


# The web address that observatory is hosted on
DOMAIN_NAME = "http://edustartup.org"

## Page header
HEADER_TEMPLATE = 'foundry/header.html'

## Favicon
FAVICON_PATH = '/site-media/rcos/favicon.ico'

# The title prepended to any RSS feeds
FEED_TITLE = "FOUNDRY"

FOOTER = 'foundry/partials/footer.html'