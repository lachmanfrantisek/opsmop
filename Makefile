PY_PACKAGE = opsmop

requirements:
	pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pypi.org --trusted-host files.pythonhosted.org

venv:
	virtualenv env -p /usr/local/bin/python3

html: cleardocs gendocs sphinx docs_publish

cleardocs:
	(rm -rf docs/build/html)
	(rm -rf docs/build/doctrees)

sphinx:
	(cd docs; make html)

gendocs:
	mkdir -p docs/source/modules/
	PYTHONPATH=. python3 -m opsmop.meta.docs.cli ../opsmop-demo/module_docs docs/source/modules

docs_publish:
	cp -a docs/build/html/* ../opsmop-docs/

indent_check:
	pep8 --select E111 opsmop/

pyflakes:
	pyflakes opsmop/

clean:
	find . -name '*.pyc' | xargs rm -r
	find . -name '__pycache__' | xargs rm -rf

todo:
	grep TODO -rn opsmop

bug:
	grep BUG -rn opsmop

fixme:
	grep FIXME -rn opsmop

isort:
	find opsmop -name '*.py' | xargs isort

gource:
	gource -s .06 -1280x720 --auto-skip-seconds .1 --hide mouse,progress,filenames --key --multi-sampling --stop-at-end --file-idle-time 0 --max-files 0  --background-colour 000000 --font-size 22 --title "OpsMop" --output-ppm-stream - --output-framerate 30 | avconv -y -r 30 -f image2pipe -vcodec ppm -i - -b 65536K movie.mp4

check-pypi-packaging:
	rm -f dist/* \
	&& python3 ./setup.py sdist bdist_wheel \
	&& pip3 install dist/*.tar.gz \
	&& ( opsmop | grep -c "opsmop - (C) 2018, Michael DeHaan LLC" ) \
	&& pip3 show $(PY_PACKAGE) \
	&& twine check ./dist/* \
	&& python3 -c "import opsmop; print(opsmop.__version__)" \
	&& pip3 show -f $(PY_PACKAGE) | ( grep test && exit 1 || :) \
