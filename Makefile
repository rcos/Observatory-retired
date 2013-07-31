
clean:
	find . -name "*.pyc" -delete

test:
	librarian-puppet install
	vagrant up
	vagrant provision
	ssh -p 2222 vagrant@localhost "/vagrant/dev/run_test.sh"

deploy:
	production/update.sh rcos.rpi.edu

.PHONY: test deploy clean
