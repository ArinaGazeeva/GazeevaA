# Руководство

## Создание ssh ключа

* Проверка на наличие ключей 
ls ~/.ssh
* Создаем ключ
ssh-keygen -t ed25519 -C "имя.фамилия@phystech.edu"
* Вывод значения ключа
cat ~/.ssh/id_ed25519.pub

## Добавление ключа на GitHub
* Добавляем ключи в агента SSH

eval "$(ssh-agent -s)"
А после добавить в агента ваш ключ при помощи команды:
ssh-add ~/.ssh/id_ed25519

Последние две команды необходимо выполнять каждый раз при перезапуске терминала.

* Проверка
ssh -T git@github.com
Она должна вернуть
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.

## Клонирование репозитория

* Это можно сделать при помощи команды, где в url вставьте адрес репозитория:
git clone url
После этого в текущей папке появится папка с названием вашего репозитория. 