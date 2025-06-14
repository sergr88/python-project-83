# Анализатор страниц

## Бейджики Hexlet
[![Actions Status](https://github.com/sergr88/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/sergr88/python-project-83/actions)

## Бейджики Qlty
[![Maintainability](https://qlty.sh/badges/8f990045-2029-40a6-976e-f5b81294b9ff/maintainability.svg)](https://qlty.sh/gh/sergr88/projects/python-project-83)
[![Code Coverage](https://qlty.sh/badges/8f990045-2029-40a6-976e-f5b81294b9ff/test_coverage.svg)](https://qlty.sh/gh/sergr88/projects/python-project-83)

## Описание
Page Analyzer – это сайт, который анализирует указанные страницы на
SEO-пригодность по аналогии с PageSpeed Insights. Развернутый сайт доступен по
адресу https://python-project-83-lsbj.onrender.com

## Требования
- Python 3.12+

## Команды
#### Запуск базы данных в окружении разработки
```shell
make db-up
```
#### Выключение и удаление базы данных в окружении разработки
```shell
make db-down
```
#### Вывод лога базы данных в окружении разработки
```shell
make db-logs
```
#### Развертывание сервиса в окружении разработки
```shell
make install
```
#### Запуск сервиса в окружении разработки
```shell
make dev
```
#### Запуск сервиса в окружении разработки через Gunicorn
```shell
make start
```
#### Развертывание сервиса в продуктивном окружении Render
```shell
make build
```
#### Запуск сервиса в продуктивном окружении Render
```shell
make render-start
```
#### Проверка линтером
```shell
make lint
```
#### Проверка линтером с исправлением замечаний
```shell
make lint-fix
```
