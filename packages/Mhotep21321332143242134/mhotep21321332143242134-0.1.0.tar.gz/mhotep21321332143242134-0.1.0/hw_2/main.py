# -*- coding: utf-8 -*-
import os
from latex_generator import *


def main():
    # Пример данных для таблицы
    data = [
        ["Header 1", "Header 2", "Header 3"],
        ["Row 1, Cell 1", "Row 1, Cell 2", "Row 1, Cell 3"],
        ["Row 2, Cell 1", "Row 2, Cell 2", "Row 2, Cell 3"],
        ["Row 3, Cell 1", "Row 3, Cell 2", "Row 3, Cell 3"]
    ]

    # Сгенерировать начало документа
    latex_code = generate_start()

    # Добавить таблицу
    latex_code += list_to_latex_table_with_document(data)

    # Добавить изображение
    latex_code += include_latex_image('carno.png', "A Lizard", 0.25)

    # Закончить документ
    latex_code += generate_end()

    # Путь к текущей директории
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "full_latex_document.tex")
    # Сохранение LaTeX кода в файл
    with open(file_path, "w") as file:
        file.write(latex_code)

    print(f"LaTeX документ был успешно сохранен в {file_path}.")


if __name__ == "__main__":
    main()
