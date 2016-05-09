all:
	chmod +x VMtranslator

tar:
	tar cvf project7.tar *.py VMtranslator README Makefile

clean:
	rm -f *.pyc
