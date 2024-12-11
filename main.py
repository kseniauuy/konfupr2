import requests
from bs4 import BeautifulSoup
import argparse

def get_dependencies(package_name):
    """
    Получить список зависимостей для указанного пакета из Alpine Linux.
    """
    url = f"https://pkgs.alpinelinux.org/package/v3.14/main/x86_64/{package_name}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка при получении данных для пакета {package_name}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    dependencies = []
    depends_section = soup.find('summary', string=lambda text: text and 'Depends' in text)

    if depends_section:
        ul = depends_section.find_next('ul')
        if ul:
            for li in ul.find_all('li'):
                dep = li.text.strip()
                if dep.startswith("so:"):
                    dep = dep[3:]  # Удаляем префикс "so:"
                    dep = dep.split('.')[0]  # Избавляемся от версии зависимости
                if dep and dep not in dependencies:
                    dependencies.append(dep)

    return dependencies


def create_dependency_graph(package_name, visited=None):
    """
    Рекурсивно строит граф зависимостей для пакета.
    В этом случае, генерируется граф для Flowchart Mermaid.
    """
    if visited is None:
        visited = set()

    if package_name in visited:
        return []

    visited.add(package_name)
    dependencies = get_dependencies(package_name)

    graph_lines = []
    for dep in dependencies:
        graph_lines.append(f"    {package_name} --> {dep}")  # Flowchart-синтаксис для Mermaid
        graph_lines.extend(create_dependency_graph(dep, visited))

    return graph_lines


def save_graph(graph_lines, output_file):
    """
    Сохраняет граф зависимостей в формате Flowchart Mermaid.
    """
    with open(output_file, 'w') as f:
        f.write('graph TD\n')
        for line in graph_lines:
            f.write(f"{line}\n")
    print(f"Граф зависимостей сохранён в файл: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Получить зависимости пакета из Alpine Linux.')
    parser.add_argument('--package', required=True, help='Название пакета')
    parser.add_argument('--output-file', required=True, help='Имя выходного файла для Flowchart диаграммы (в формате .mermaid)')

    args = parser.parse_args()

    graph_lines = create_dependency_graph(args.package)
    save_graph(graph_lines, args.output_file)


if __name__ == "__main__":
    main()
