
test:
	librarian-puppet install
	vagrant up
	vagrant provision

.PHONY: test
