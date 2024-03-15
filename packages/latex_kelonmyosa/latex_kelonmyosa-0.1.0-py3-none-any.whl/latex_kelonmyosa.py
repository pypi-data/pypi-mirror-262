def create_latex_document() -> str:
    """
    Создает начальное состояние LaTeX документа.
    """
    return "\\documentclass[a4paper]{article}\n\\usepackage{graphicx}\n\\begin{document}\n"


def add_table(content: str, table: list[list]) -> str:
    """
    Добавляет таблицу в LaTeX документ.

    :param content: Текущее содержимое документа.
    :param table: Двумерный список, представляющий таблицу.
    :return: Обновленное содержимое документа.
    """
    header = table[0]
    rows = table[1:]

    table_code = "\\begin{tabular}{|" + "l|" * len(header) + "}\n\\hline\n"
    table_code += " & ".join(header) + " \\\\\n\\hline\n"
    for row in rows:
        table_code += " & ".join(row) + " \\\\\n\\hline\n"
    table_code += "\\end{tabular}\n"

    return content + table_code


def add_image(content: str, filepath: str, width: str = "\\textwidth") -> str:
    """
    Добавляет изображение в LaTeX документ.

    :param content: Текущее содержимое документа.
    :param filepath: Путь к изображению.
    :param width: Ширина изображения в документе.
    :return: Обновленное содержимое документа.
    """
    return content + f"\\includegraphics[width={width}]{{{filepath}}}\n"


def add_empty_line(content: str) -> str:
    """
    Добавляет пустую строку в LaTeX документ.

    :param content: Текущее содержимое документа.
    :return: Обновленное содержимое документа.
    """
    return content + "\\newline\n\\vspace{1em}\n"


def end_document(content: str) -> str:
    """
    Завершает LaTeX документ (Вызывать обязательно в конце документа).

    :param content: Текущее содержимое документа.
    :return: Завершенное содержимое документа.
    """
    return content + "\\end{document}"


def save_document(content: str, path: str):
    """
    Сохраняет LaTeX документ.

    :param content: Содержимое документа.
    :param path: Путь сохранения документа (Название файла должно заканчиваться '.tex').
    """
    with open(path, "w") as file:
        file.write(content)
