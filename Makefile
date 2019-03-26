ENVS := py27,py36

addon_xml = addon.xml

# Collect information to build as sensible package name
name = $(shell xmllint --xpath 'string(/addon/@id)' $(addon_xml))
version = $(shell xmllint --xpath 'string(/addon/@version)' $(addon_xml))
git_hash = $(shell git rev-parse --short HEAD)

zip_name = $(name)-$(version)-$(git_hash).zip
include_files = addon.py addon.xml LICENSE README.md resources/ service.py
include_paths = $(patsubst %,$(name)/%,$(include_files))
exclude_files = \*.new \*.orig
zip_dir = $(name)/

.PHONY: test

package: zip

clean:
	@echo -e "\e[1;37m=\e[1;34m Clean up project directory\e[0m"
	find . -name '*.pyc' -delete
	@echo -e "\e[1;37m=\e[1;34m Finished cleaning up.\e[0m"

test: unittest
	@echo -e "\e[1;37m=\e[1;34m Starting tests\e[0m"
	pylint *.py
	pylint resources/lib/*/*.py
	tox -e $(ENVS)
	@echo -e "\e[1;37m=\e[1;34m Tests finished successfully.\e[0m"

unittest:
	@echo -e "\e[1;37m=\e[1;34m Starting unit tests\e[0m"
	PYTHONPATH=$(pwd) python test/vrtplayertests.py
	@echo -e "\e[1;37m=\e[1;34m Unit tests finished successfully.\e[0m"

zip: test clean
	@echo -e "\e[1;37m=\e[1;34m Building new package\e[0m"
	rm -f ../$(zip_name)
	cd ..; zip -r $(zip_name) $(include_paths) -x $(exclude_files)
	@echo -e "\e[1;37m=\e[1;34m Successfully wrote package as: \e[1;37m../$(zip_name)\e[0m"
