DIST = dist

server_wheel = ${dist_dir}/minesweeper-multi-server.whl
client-tar = ${dist_dir}/minesweeper-multi-client-js.tar.gz

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simple help recipe                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
.PHONY: help

help:
	@echo 'USAGE: make TARGET [VARS...]'
	@echo
	@echo 'Targets:'
	@echo '  clean        remove all project or build generated files'
	@echo '  client-js    build source and docker file for the javascript client'
	@echo '  server       build the source and dockerfile for the server'
	@echo
	@echo 'Variables:'
	@echo '  DIST    the path where distrobution files should be stored.'


${DIST}:
	mkdir --parents "$@"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Recipes for docker images                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
.PHONY: docker-client-js docker-server

client-js: ${server_wheel}
	docker build --file docker/client/Dockerfile ${DIST}

server:: ${client-tar}
	docker build --file docker/server/Dockerfile ${DIST}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Recipes for source builds                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
${server_wheel}:
	@echo '=== [server_wheel] ==='

${client_tar}:
	@echo '=== [client_tar] ==='

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Recipes for source builds                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
clean:
	rm --recursive ${dist_dir}
	find . -name __pycache__ -exec rm --recursive '{}' +
