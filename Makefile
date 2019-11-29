export PYTHONPATH := $(CURDIR)/resources/lib:$(CURDIR)/test
PYTHON := python

name = $(shell xmllint --xpath 'string(/addon/@id)' addon.xml)
version = $(shell xmllint --xpath 'string(/addon/@version)' addon.xml)
git_branch = $(shell git rev-parse --abbrev-ref HEAD)
git_hash = $(shell git rev-parse --short HEAD)

zip_name = $(name)-$(version)-$(git_branch)-$(git_hash).zip
include_files = addon.xml LICENSE README.md resources/
include_paths = $(patsubst %,$(name)/%,$(include_files))
exclude_files = \*.new \*.orig \*.pyc \*.pyo
zip_dir = $(name)/

languages = $(filter-out en_gb, $(patsubst resources/language/resource.language.%, %, $(wildcard resources/language/*)))

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
	$(PYTHON) -m tox -q

pylint:
	@echo -e "$(white)=$(blue) Starting sanity pylint test$(reset)"
	$(PYTHON) -m pylint resources/lib/ test/

language:
	@echo -e "$(white)=$(blue) Starting language test$(reset)"
	@-$(foreach lang,$(languages), \
		msgcmp resources/language/resource.language.$(lang)/strings.po resources/language/resource.language.en_gb/strings.po; \
	)

addon: clean
	@echo -e "$(white)=$(blue) Starting sanity addon tests$(reset)"
	kodi-addon-checker . --branch=krypton
	kodi-addon-checker . --branch=leia

unit: clean
	@echo -e "$(white)=$(blue) Starting unit tests$(reset)"
	-pkill -ef '$(PYTHON) -m proxy'
	$(PYTHON) -m proxy &
	$(PYTHON) -m unittest discover
	pkill -ef '$(PYTHON) -m proxy'

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
	curl --data-binary @.github/codecov.yml https://codecov.io/validate

clean:
	find . -name '*.pyc' -type f -delete
	find . -name '*.pyo' -type f -delete
	find . -name '__pycache__' -type d -delete
	rm -rf .pytest_cache/ .tox/
	rm -f *.log test/userdata/tokens/*.tkn
