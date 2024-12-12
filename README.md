# Домашнее задание №2 Вариант 29
___
## Описание
Этот проект представляет собой инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости
___
## Использование
Перед началом использования файла необходимо загрузить библиотеку requests, bs4.
`pip install requests bs4`

## Тестирование программы
Запуск: в качестве примера возьмем пакет curl

![test](https://github.com/kseniauuy/konfupr2/blob/main/img/zapusk.png?raw=true)

Получаем на выходе изображение графа:

![resultpng](https://github.com/kseniauuy/konfupr2/blob/main/img/result.png?raw=true)

Видим ошибку 404, возникающую в связи с тем что обработка прямых зависимостей не проводится, но программа работает.

##Функции программы:
![codepng](https://github.com/kseniauuy/konfupr2/blob/main/img/code1.png?raw=true)

![codepng](https://github.com/kseniauuy/konfupr2/blob/main/img/code2.png?raw=true)

![codepng](https://github.com/kseniauuy/konfupr2/blob/main/img/code3.png?raw=true)

![codepng](https://github.com/kseniauuy/konfupr2/blob/main/img/code4.png?raw=true)

## Тестирование программы c помощью pytest

![pytest](https://github.com/kseniauuy/konfupr2/blob/main/img/pytest.png?raw=true)
