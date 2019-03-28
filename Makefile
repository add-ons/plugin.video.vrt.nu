ENVS := py27,py36

addon_xml = addon.xml

# Collect information to build as sensible package name
name = $(shell xmllint --xpath 'string(/addon/@id)' $(addon_xml))
version = $(shell xmllint --xpath 'string(/addon/@version)' $(addon_xml))
git_hash = $(shell git rev-parse --short HEAD)

zip_name = $(name)-$(version)-$(git_hash).zip
include_files = addon.py addon.xml LICENSE README.md resources/ service.py
include_paths = $(patsubst %,$(name)/%,$(include_files))
exclude_files = \*.new \*.orig \*.pyc
zip_dir = $(name)/

blue = \e[1;34m
white = \e[1;37m
reset = \e[0m

.PHONY: test

package: zip

test: sanity unit

sanity:
	@echo -e "$(white)=$(blue) Starting sanity tests$(reset)"
	pylint *.py
	pylint resources/lib/*/*.py
	tox -e $(ENVS)
	@echo -e "$(white)=$(blue) Sanity tests finished successfully.$(reset)"

unit:
	@echo -e "$(white)=$(blue) Starting unit tests$(reset)"
	PYTHONPATH=$(pwd) python test/vrtplayertests.py
	@echo -e "$(white)=$(blue) Unit tests finished successfully.$(reset)"

zip: test
	@echo -e "$(white)=$(blue) Building new package$(reset)"
	rm -f ../$(zip_name)
	cd ..; zip -r $(zip_name) $(include_paths) -x $(exclude_files)
	@echo -e "$(white)=$(blue) Successfully wrote package as: $(white)../$(zip_name)$(reset)"
