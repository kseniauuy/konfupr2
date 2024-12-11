import pytest
from unittest.mock import patch
from io import StringIO
from main import get_dependencies, create_dependency_graph, save_graph

def test_get_dependencies():
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = b"""<html>
            <body>
                <summary>Depends</summary>
                <ul>
                    <li>so:libc.so.6</li>
                    <li>so:libcurl.so.4</li>
                    <li>so:libcrypto.so.1.1</li>
                </ul>
            </body>
        </html>"""

        dependencies = get_dependencies('curl')

    assert dependencies == ['libc', 'libcurl', 'libcrypto']

def test_create_dependency_graph():
    with patch('main.get_dependencies') as mock_get_dependencies:
        mock_get_dependencies.return_value = ['libc', 'libcurl', 'libcrypto', 'libz', 'libnghttp2']

        graph = create_dependency_graph('curl')

        expected_graph = [
            '    curl --> libc',
            '    libc --> libc',
            '    libc --> libcurl',
            '    libcurl --> libc',
            '    libcurl --> libcurl',
            '    libcurl --> libcrypto',
            '    libcrypto --> libc',
            '    libcrypto --> libcurl',
            '    libcrypto --> libcrypto',
            '    libcrypto --> libz',
            '    libz --> libc',
            '    libz --> libcurl',
            '    libz --> libcrypto',
            '    libz --> libz',
            '    libz --> libnghttp2',
            '    libnghttp2 --> libc',
            '    libnghttp2 --> libcurl',
            '    libnghttp2 --> libcrypto',
            '    libnghttp2 --> libz',
            '    libnghttp2 --> libnghttp2',
            '    libcrypto --> libnghttp2',
            '    libcurl --> libz',
            '    libcurl --> libnghttp2',
            '    libc --> libcrypto',
            '    libc --> libz',
            '    libc --> libnghttp2',
            '    curl --> libcurl',
            '    curl --> libcrypto',
            '    curl --> libz',
            '    curl --> libnghttp2'
        ]

        assert graph == expected_graph



def test_save_graph():

    with patch('builtins.open', return_value=StringIO()) as mock_open:
        graph_lines = [
            '    curl --> libc',
            '    curl --> libcurl',
            '    curl --> libcrypto'
        ]
        output_file = 'test_graph.mermaid'

        save_graph(graph_lines, output_file)

        mock_open.return_value.seek(0)
        content = mock_open.return_value.read().strip()

        expected_content = "erDiagram\n    curl --> libc\n    curl --> libcurl\n    curl --> libcrypto"
        assert content == expected_content

def test_full_graph_creation_and_save():
    with patch('main.get_dependencies') as mock_get_dependencies, patch('builtins.open', return_value=StringIO()) as mock_open:
        mock_get_dependencies.return_value = ['libc', 'libcurl', 'libcrypto', 'libz', 'libnghttp2']

        package_name = 'curl'
        output_file = 'test_graph.mermaid'

        graph_lines = create_dependency_graph(package_name)

        expected_graph_lines = [
            '    curl --> libc',
            '    libc --> libc',
            '    libc --> libcurl',
            '    libcurl --> libc',
            '    libcurl --> libcurl',
            '    libcurl --> libcrypto',
            '    libcrypto --> libc',
            '    libcrypto --> libcurl',
            '    libcrypto --> libcrypto',
            '    libcrypto --> libz',
            '    libz --> libc',
            '    libz --> libcurl',
            '    libz --> libcrypto',
            '    libz --> libz',
            '    libz --> libnghttp2',
            '    libnghttp2 --> libc',
            '    libnghttp2 --> libcurl',
            '    libnghttp2 --> libcrypto',
            '    libnghttp2 --> libz',
            '    libnghttp2 --> libnghttp2',
            '    libcrypto --> libnghttp2',
            '    libcurl --> libz',
            '    libcurl --> libnghttp2',
            '    libc --> libcrypto',
            '    libc --> libz',
            '    libc --> libnghttp2',
            '    curl --> libcurl',
            '    curl --> libcrypto',
            '    curl --> libz',
            '    curl --> libnghttp2'
        ]

        assert graph_lines == expected_graph_lines

        save_graph(graph_lines, output_file)
        mock_open.return_value.seek(0)
        content = mock_open.return_value.read().strip()
        expected_content = "erDiagram\n    curl --> libc\n    curl --> libcurl\n    curl --> libcrypto\n    curl --> libz\n    curl --> libnghttp2"
        assert content == expected_content
