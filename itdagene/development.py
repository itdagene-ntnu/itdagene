from itdagene.dev_no_toolbar import *

TOOLBAR = True
THUMBNAIL_DEBUG = True
POSTGRESQL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOTPATH + '/project.db'
    }
}

#Django debug toolbar
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'cache_panel.CachePanel',
)

#To show debug toolbar or not. Only shows on debug == True
def custom_show_toolbar(request):
	return DEBUG

DEBUG_TOOLBAR_CONFIG = {
	'SHOW_TOOLBAR_CALLBACK' : custom_show_toolbar,
	'HIDE_DJANGO_SQL' : False,
	'INTERCEPT_REDIRECTS' : False, #Set to True if you want to see requests before you are redirected
	}

#Toolbar
INSTALLED_APPS += ('debug_toolbar',)