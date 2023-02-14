PREFIX ?= /usr
OPTDIR ?= /opt

BINDIR = $(PREFIX)/bin
DATDIR = $(OPTDIR)/openai

all: build install

build:
	termux-fix-shebang openai_chat.py
	termux-fix-shebang openai-cli-client

install:
	mkdir -p $(DATDIR)
	install -Dm755 -t $(BINDIR) ./openai-cli-client
	install -Dm755 -t $(DATDIR) ./openai_chat.py

uninstall:
	rm $(BINDIR)/openai-cli-client
	rm -r $(DATDIR)

.PHONY: all build install uninstall
