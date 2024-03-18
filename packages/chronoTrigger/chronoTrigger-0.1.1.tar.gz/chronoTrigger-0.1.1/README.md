# ChronoTrigger

## A Python library to facilitate working with intervals.

### Installation:
To install ChronoTrigger, simply use pip:
```bash
pip install chronoTrigger
```

### Usage:
Import the necessary functions from the library to start using them in your code.
```python
from chronoTrigger import set_interval, clear_interval, set_timeout, clear_timeout

def say_hello(name):
    print(f"Hello, {name}!")

# This will call the say_hello function every 1 second with "Alex" as the parameter.
interval = set_interval(say_hello, 1, "Alex")
# This will clear the interval after 5 seconds.
set_timeout(clear_interval, 5, interval)
```
#### Output:
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=16&duration=1000&pause=1000&color=ACB6F7&multiline=true&random=false&width=435&height=125&lines=Hello%2C+Alex!;Hello%2C+Alex!;Hello%2C+Alex!;Hello%2C+Alex!)](https://git.io/typing-svg)

---

# ChronoTrigger

## Python библиотека для облегчения работы с интервалами.

### Установка:
Для установки ChronoTrigger просто используйте pip:
```bash
pip install chronoTrigger
```

### Использование:
Импортируйте необходимые функции из библиотеки, чтобы начать их использовать в вашем коде.
```python
from chronoTrigger import set_interval, clear_interval, set_timeout, clear_timeout

def say_hello(name):
    print(f"Привет, {name}!")

# Это будет вызывать функцию say_hello каждую 1 секунду с параметром "Alex".
interval = set_interval(say_hello, 1, "Alex")
# Это остановит интервал через 5 секунд.
set_timeout(clear_interval, 5, interval)
```
#### Вывод:
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=16&duration=1000&pause=1000&color=ACB6F7&multiline=true&random=false&width=435&height=125&lines=Привет%2C+Alex!;Привет%2C+Alex!;Привет%2C+Alex!;Привет%2C+Alex!)](https://git.io/typing-svg)
