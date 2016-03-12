#
# Executables and paths
#

STYLUS     = node_modules/.bin/stylus
UGLIFY     = node_modules/.bin/uglifyjs
BROWSERIFY = node_modules/.bin/browserify
WATCHIFY   = node_modules/.bin/watchify
NIB        = node_modules/nib/lib

#
# The main CSS and JS files
#

CSS_MAIN   = itdagene/assets/frontend/styl/style.styl
JS_MAIN    = itdagene/assets/frontend/js/index.js

#
# All CSS and JS files (used for file watching)
#

CSS        = $(shell find itdagene/assets/frontend/styl -name "*.styl")
JS         = $(shell find itdagene/assets/frontend/js -name "*.js")

#
# Compiled CSS and JS Files
#

BUILD_CSS  = itdagene/assets/frontend/itdagene.css
BUILD_JS   = itdagene/assets/frontend/itdagene.js

#
# Browserify Transforms
# See https://github.com/substack/node-browserify/wiki/list-of-transforms
#

TRANSFORMS = -t [ reactify --harmony ]

#
# Default task
#

all: $(BUILD_CSS) $(BUILD_JS)

install: node_modules bower

node_modules: package.json
	@npm install

bower: bower.json
	@bower install

local-dev:
	echo "from itdagene.settings.dev import *" > itdagene/settings/local.py
#
# Build CSS files
#

$(BUILD_CSS): $(CSS)
ifneq ($(NODE_ENV), development)
	$(STYLUS) --include $(NIB) \
	--include itdagene/assets/frontend/styl \
	--compress < $(CSS_MAIN) > $(BUILD_CSS)
else
	$(STYLUS) --include $(NIB) \
	--include itdagene/assets/frontend/styl \
	--include-css < $(CSS_MAIN) > $(BUILD_CSS)
endif

#
# Build JavaScript files
#

$(BUILD_JS): $(JS)
ifneq ($(NODE_ENV), development)
	$(BROWSERIFY) $(TRANSFORMS) $(JS_MAIN) | $(UGLIFY) > $(BUILD_JS)
else
	$(BROWSERIFY) $(TRANSFORMS) $(JS_MAIN) > $(BUILD_JS)
endif

#
# Watchify is extremely fast compared to running browserify on file changes.
#

watchify:
	$(WATCHIFY) $(TRANSFORMS) $(JS_MAIN) -v -o $(BUILD_JS)

#
# A avoid to avoid «Nothing to be done for all messages»
#

watch-css:
	watch --interval=1 $(MAKE) $(BUILD_CSS)

#
#
#

watch:
	@forego start

#
# Remove build files
#

clean:
	rm -f $(BUILD_CSS) $(BUILD_JS)

itdagene/settings/local.py:
	touch itdagene/settings/local.py

#
# Non-files are PHONY targets
#

.PHONY: clean itdagene/settings/local.py
