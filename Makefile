ENVS := flake8,py27,py35,py36,py37,py38
PYTHON := python
export PYTHONPATH := $(CURDIR)/resources/lib:$(CURDIR)/test
addon_xml := addon.xml

# Collect information to build as sensible package name
name = $(shell xmllint --xpath 'string(/addon/@id)' $(addon_xml))
version = $(shell xmllint --xpath 'string(/addon/@version)' $(addon_xml))
git_branch = $(shell git rev-parse --abbrev-ref HEAD)
git_hash = $(shell git rev-parse --short HEAD)

zip_name = $(name)-$(version)-$(git_branch)-$(git_hash).zip
include_files = addon.xml LICENSE README.md resources/
include_paths = $(patsubst %,$(name)/%,$(include_files))
exclude_files = \*.new \*.orig \*.pyc \*.pyo
zip_dir = $(name)/

blue = \e[1;34m
white = \e[1;37m
reset = \e[0;39m

.PHONY: test

all: test zip

package: zip

test: sanity unit run

sanity: tox pylint language

tox:
	@echo -e "$(white)=$(blue) Starting sanity tox test$(reset)"
	tox -q -e $(ENVS)

pylint:
	@echo -e "$(white)=$(blue) Starting sanity pylint test$(reset)"
	$(PYTHON) /usr/bin/pylint resources/lib/ test/

pylint-warnings:
	@echo -e "$(white)=$(blue) Starting sanity pylint test$(reset)"
	$(PYTHON) /usr/bin/pylint -e useless-suppression resources/lib/ test/

language:
	@echo -e "$(white)=$(blue) Checking translations$(reset)"
	msgcmp resources/language/resource.language.nl_nl/strings.po resources/language/resource.language.en_gb/strings.po

addon: clean
	@echo -e "$(white)=$(blue) Starting sanity addon tests$(reset)"
	$(PYTHON) /usr/bin/kodi-addon-checker . --branch=krypton
	$(PYTHON) /usr/bin/kodi-addon-checker . --branch=leia

unit: clean
	@echo -e "$(white)=$(blue) Starting unit tests$(reset)"
	-pkill -ef /usr/bin/proxy.py
	$(PYTHON) /usr/bin/proxy.py &
	$(PYTHON) -m unittest discover
	pkill -ef /usr/bin/proxy.py

run:
	@echo -e "$(white)=$(blue) Run CLI$(reset)"
	$(PYTHON) resources/lib/service_entry.py
	$(PYTHON) test/run.py /

zip: clean
	@echo -e "$(white)=$(blue) Building new package$(reset)"
	@rm -f ../$(zip_name)
	cd ..; zip -r $(zip_name) $(include_paths) -x $(exclude_files)
	@echo -e "$(white)=$(blue) Successfully wrote package as: $(white)../$(zip_name)$(reset)"

codecov:
	@echo -e "$(white)=$(blue) Test .codecov.yml syntax$(reset)"
	curl --data-binary @.codecov.yml https://codecov.io/validate

clean:
	find . -name '*.pyc' -type f -delete
	find . -name '*.pyo' -type f -delete
	find . -name '__pycache__' -type d -delete
	rm -rf .pytest_cache/ .tox/
	rm -f *.log test/userdata/tokens/*.tkn
