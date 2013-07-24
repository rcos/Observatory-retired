
test:
	librarian-puppet install
	vagrant up
	vagrant provision

deploy:
	production/update.sh rcos.rpi.edu

.PHONY: test deploy
