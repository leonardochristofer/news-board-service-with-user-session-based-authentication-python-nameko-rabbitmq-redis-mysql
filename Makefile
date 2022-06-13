# Nameko Stuff
NAMEKOCMD=nameko

NAMEKORUN=$(NAMEKOCMD) run

run-user:
	$(NAMEKORUN) user_access.service

run-news:
	$(NAMEKORUN) news_board.service

run-gateway:
	$(NAMEKORUN) gateway.service