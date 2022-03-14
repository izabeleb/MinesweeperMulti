DIST = dist

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simple help recipe                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
.PHONY: help

help:
	@echo 'USAGE: make TARGET [VARS...]'
	@echo
	@echo 'Targets:'
	@echo '  all          build all docker images'
	@echo '  client-js    build docker image for the javascript client'
	@echo '  server       build docker image for the server'
	@echo '  clean        remove all project or build generated files'
	@echo
	@echo 'Variables:'
	@echo '  DIST    the path where distrobution files should be stored.'


${DIST}:
	mkdir --parents "$@"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Recipes for docker images                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
.PHONY: all client-js server

all: server client-js

server:
	make --directory server docker

client-js:
	make --directory client-js docker

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Recipes for cleanup                                                         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
clean:
