ADDON_XML = plugin.video.vrt.nu/addon.xml

# Collect information to build as sensible package name
NAME = $(shell xmllint --xpath 'string(/addon/@id)' $(ADDON_XML))
VERSION = $(shell xmllint --xpath 'string(/addon/@version)' $(ADDON_XML))
GIT_HASH = $(shell git rev-parse --short HEAD)

ZIP_NAME = $(NAME)-$(VERSION)-$(GIT_HASH).zip
EXCLUDE_FILES = $(NAME).pyproj vrtnutests
ZIP_DIR = $(NAME)

all: zip
package: zip

zip:
	@echo -e "\e[1;37m=\e[1;34m Building new package\e[0m"
	rm -f $(ZIP_NAME)
	zip -qr $(ZIP_NAME) $(ZIP_DIR) -x $(EXCLUDE_FILES)
	@echo -e "\e[1;37m=\e[1;34m Successfully wrote package as \e[1;37m$(ZIP_NAME)\e[0m"
