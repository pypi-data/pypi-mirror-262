
def list_to_latex_table_with_document(data):
    """
    Преобразует двумерный список в полный документ LaTeX, включая таблицу.
    """
    # Преамбула LaTeX документа с поддержкой кириллицы
    latex_document = [
        "\\begin{table}[]\n",
        "\\begin{tabular}{" + "|l" * len(data[0]) + "|}\n",
        "\\hline\n"
    ]

    # Добавление данных таблицы
    for row in data:
        latex_document.append(" & ".join(row) + " \\\\\n\\hline\n")

    # Закрытие таблицы и документа
    latex_document.extend([
        "\\end{tabular}\n",
        "\\end{table}\n",
        "\n",
    ])

    return "".join(latex_document)

def include_latex_image(image_path, caption="Figure", width="0.25"):
    """
    Генерирует LaTeX код для включения изображения в документ.

    :param image_path: Путь к изображению.
    :param caption: Подпись к изображению.
    :param width: Ширина изображения в долях от ширины строки (по умолчанию 25%).
    :return: Строка с кодом LaTeX.
    """
    latex_image = f"""
\\begin{{figure}}[h]
    \\centering
    \\includegraphics[width={width}\\linewidth]{{{image_path}}}
    \\caption{{{caption}}}
\\end{{figure}}
"""
    return latex_image

def generate_start():
    latex_code = '\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}'
    return latex_code


def generate_end():
    latex_code = '\\end{document}'
    return latex_code