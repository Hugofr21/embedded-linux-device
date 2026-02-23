.PHONY: all clear test

clear:
	@echo "Removendo artefatos temporários e cache Python..."
	rm -f *.pyc
	rm -rf __pycache__

test:
	@echo "Executando o script de monitoramento BPF com elevação de privilégio..."
	sudo python3 monitor.py