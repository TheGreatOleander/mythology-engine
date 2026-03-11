.PHONY: install run status release demo

install:
	python -m pip install -e .

run:
	mythology --mode manual --action full-cycle

status:
	mythology --mode manual --action status

release:
	mythology --mode assisted --action release-package

demo:
	python runtime/demo_cycle.py

providers:
	mythology --mode manual --action providers

bootstrap provider-test episode-test audio-test platforms publish-sim:
	python bootstrap provider-test episode-test audio-test platforms publish-sim/tools/run_bootstrap provider-test episode-test audio-test platforms publish-sim.py

provider-test episode-test audio-test platforms publish-sim:
	mythology --mode manual --action provider-test episode-test audio-test platforms publish-sim

episode-test audio-test platforms publish-sim:
	mythology --mode manual --action episode-test audio-test platforms publish-sim

audio-test platforms publish-sim:
	mythology --mode manual --action audio-test platforms publish-sim

platforms:
	mythology --action platforms

publish-sim:
	mythology --action publish-sim
