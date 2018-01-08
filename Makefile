BUILD_CSS  = itdagene/assets/frontend/itdagene.css
BUILD_JS   = itdagene/assets/frontend/itdagene.js

clean:
	rm -f $(BUILD_CSS) $(BUILD_JS)

itdagene/settings/local.py:
	touch itdagene/settings/local.py

#
# Non-files are PHONY targets
#

.PHONY: clean itdagene/settings/local.py
