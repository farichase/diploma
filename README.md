# REFAL SMT-SCPstr


### Запуск
```sh
	git clone https://github.com/farichase/diploma.git
	cd diploma/my-app
	chmod +x setup.sh
	./setup.sh
	npm install
	sudo docker build -t "my_image" .
```	
##### Запуск сервера (консоль №1):
```sh
	cd diploma/my-app/backend
	sudo node app
```	
##### Запуск клиента (консоль №2):
```sh
	cd diploma/my-app
	npm start
```	

