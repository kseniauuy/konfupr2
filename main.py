import requests
from bs4 import BeautifulSoup
import argparse

def get_dependencies(package_name):
    """
    Получает список зависимостей для указанного пакета из Alpine Linux.

    Эта функция отправляет запрос на страницу пакета на сайте Alpine Linux, 
    парсит HTML-страницу с помощью BeautifulSoup и извлекает список зависимостей.
    Зависимости, которые начинаются с "so:" (указывают на shared object, т.е. библиотеки),
    обрабатываются и добавляются в итоговый список.

    Аргументы:
    package_name (str): Название пакета, для которого нужно получить зависимости.

    Возвращает:
    list: Список зависимостей (названия пакетов), или пустой список в случае ошибки.
    """
    url = f"https://pkgs.alpinelinux.org/package/v3.14/main/x86_64/{package_name}"
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code != 200:
        print(f"Ошибка при получении данных для пакета {package_name}: {response.status_code}")
        return []

    # Парсинг HTML-страницы с помощью BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    dependencies = []
    # Ищем секцию, где указаны зависимости пакета
    depends_section = soup.find('summary', string=lambda text: text and 'Depends' in text)

    if depends_section:
        ul = depends_section.find_next('ul')  # Находим список зависимостей
        if ul:
            # Проходим по всем элементам списка и извлекаем название зависимости
            for li in ul.find_all('li'):
                dep = li.text.strip()
                if dep.startswith("so:"):  # Если зависимость является библиотекой (so:), обрабатываем
                    dep = dep[3:]  # Убираем префикс "so:"
                    dep = dep.split('.')[0]  # Убираем версию библиотеки
                if dep and dep not in dependencies:  # Добавляем зависимость в список, если её ещё нет
                    dependencies.append(dep)

    return dependencies


def create_dependency_graph(package_name, visited=None):
    """
    Рекурсивно строит граф зависимостей для пакета.

    Эта функция создаёт граф зависимостей в формате Flowchart Mermaid для визуализации. 
    Для каждого пакета она вызывает `get_dependencies`, чтобы получить его зависимости, 
    и рекурсивно строит граф для всех зависимых пакетов.

    Аргументы:
    package_name (str): Название пакета, для которого нужно создать граф зависимостей.
    visited (set): Множество посещённых пакетов, чтобы избежать зацикливания в графе.

    Возвращает:
    list: Список строк, представляющих связи между пакетами в формате Mermaid.
    """
    if visited is None:
        visited = set()

    # Если пакет уже был посещён, избегаем зацикливания
    if package_name in visited:
        return []

    # Добавляем пакет в посещённые
    visited.add(package_name)
    # Получаем зависимости для текущего пакета
    dependencies = get_dependencies(package_name)

    # Список строк для графа
    graph_lines = []
    # Для каждой зависимости строим связь в графе
    for dep in dependencies:
        graph_lines.append(f"    {package_name} --> {dep}")  # Flowchart-синтаксис для Mermaid
        # Рекурсивно добавляем зависимости для текущей зависимости
        graph_lines.extend(create_dependency_graph(dep, visited))

    return graph_lines


def save_graph(graph_lines, output_file):
    """
    Сохраняет граф зависимостей в файл в формате Flowchart Mermaid.

    Эта функция сохраняет сгенерированный граф зависимостей в файл с расширением .mermaid.

    Аргументы:
    graph_lines (list): Список строк, представляющих граф зависимостей в формате Mermaid.
    output_file (str): Путь к выходному файлу, в который нужно записать граф.
    """
    with open(output_file, 'w') as f:
        f.write('graph TD\n')  # Заголовок для Mermaid-графа
        for line in graph_lines:
            f.write(f"{line}\n")  # Записываем каждую строку в файл

    print(f"Граф зависимостей сохранён в файл: {output_file}")


def main():
    """
    Основная функция, которая обрабатывает аргументы командной строки и вызывает соответствующие функции.

    Эта функция использует argparse для получения аргументов из командной строки, 
    запускает процесс получения зависимостей для указанного пакета и сохраняет результат в файл.

    Используется:
    - `--package`: Название пакета, для которого нужно получить зависимости.
    - `--output-file`: Имя файла, в который будет сохранён граф зависимостей в формате Mermaid.
    """
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Получить зависимости пакета из Alpine Linux.')
    parser.add_argument('--package', required=True, help='Название пакета')
    parser.add_argument('--output-file', required=True, help='Имя выходного файла для Flowchart диаграммы (в формате .mermaid)')

    # Разбор аргументов
    args = parser.parse_args()

    # Строим граф зависимостей для указанного пакета
    graph_lines = create_dependency_graph(args.package)
    
    # Сохраняем граф в файл
    save_graph(graph_lines, args.output_file)


if __name__ == "__main__":
    main()
