import argparse
import pandas as pd


class LatexGenerator:
    """
    Класс для генерации LaTeX кода таблиц и изображений.
    """
    def generate_latex_table(self, data, caption="", label=""):
        """
        Утилита генерирует код LaTeX для таблицы\n
        из заданного двумерного списка данных.

        Аргументы:
            data (list of lists): Входные данные для таблицы.
                Каждый внутренний список представляет собой строку таблицы.
            caption (str, optional): Подпись к таблице.
            label (str, optional): Метка для ссылки на таблицу.

        Возвращает:
            str: Строка, содержащая код LaTeX для сгенерированной таблицы
        """

        rows = ["\t\t" + " & ".join(str(cell) for cell in row) +
                " \\\ \hline\n" for row in data]
        table_content = "".join(rows)

        latex_code = (
            "\\begin{table}\n"
            "\t\\centering\n"
            "\t\\begin{tabular}{|" + "|".join(
                "c" * len(data[0])
                ) + "|} \\hline\n"
            + table_content
            + "\t\\end{tabular}\n"
            + (
                (f"\t\\caption{{{caption}}}\n")
                if caption else "\t\\caption{Caption}\n"
               )
            + (
                (f"\t\\label{{{label}}}\n")
                if label else "\t\\label{tab:my_label}\n"
               )
            + "\\end{table}"
            )

        return latex_code

    def generate_latex_figure(self, filename, caption="", label=""):
        """
        Утилита генерирует код LaTeX для вставки картинки.\n
        Аргументы:
            filename (str): Имя файла изображения.\n
            caption (str): Подпись к изображению.\n
            label (str): Метка для ссылки на изображение.

        Возвращает:
            str: Строка, содержащая код LaTeX для вставки картинки
        """

        latex_code = (
            "\\begin{figure}[htbp]\n"
            "\t\\centering\n"
            f"\t\\includegraphics[width=0.5\linewidth]{{{filename}}}\n"
            + (
                (f"\t\\caption{{{caption}}}\n")
                if caption else "\t\\caption{Caption}\n"
               )
            + (
                (f"\t\\label{{{label}}}\n")
                if label else "\t\\label{fig:enter-label}\n"
               )
            + "\\end{figure}"
            )

        return latex_code

    def main(self,
             file_path,
             caption_tab,
             label_tab,
             image_filename,
             caption_fig,
             label_fig):
        #file_path = "table_data.xlsx"  # todo: прописать переменные окружения
        #caption_tab = "Example Table"  # todo: прописать переменные окружения
        #label_tab = "tab:example"  # todo: прописать переменные окружения

        #image_filename = "kitty.jpg"  # todo: прописать переменные окружения
        #caption_fig = "Example Image"  # todo: прописать переменные окружения
        #label_fig = "fig:example"  # todo: прописать переменные окружения

        # Чтение данных таблицы из файла
        df = pd.read_excel(file_path)
        table_data = df.values.tolist()

        # Генерация LaTeX кода для таблицы
        table_latex = latex_gen.generate_latex_table(table_data,
                                                     caption=caption_tab,
                                                     label=label_tab)

        # Генерация LaTeX кода для изображения
        figure_latex = latex_gen.generate_latex_figure(image_filename,
                                                       caption=caption_fig,
                                                       label=label_fig)

        # Соединяем код таблицы и код картинки
        full_latex_code = table_latex + "\n\n" + figure_latex

        # Сохраняем LaTeX в файл
        with open("artifacts/test.tex", "w") as file:
            file.write(full_latex_code)

        print("LaTeX таблица и картинка успешно сохранены в файле 'test.tex'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Сгенерировать LaTeX')

    parser.add_argument('--t',
                        type=str,
                        help='Путь к файлу Excel')
    parser.add_argument('--cap_t',
                        type=str,
                        help='Заголовок таблицы')
    parser.add_argument('--lab_t',
                        type=str,
                        help='Метка ссылки таблицы')
    parser.add_argument('--im',
                        type=str,
                        help='Название изображения')
    parser.add_argument('--cap_im',
                        type=str,
                        help='Заголовок изображения')
    parser.add_argument('--lab_im',
                        type=str,
                        help='Метка ссылки изображения')

    args = parser.parse_args()

    latex_gen = LatexGenerator()
    latex_gen.main(args.t,
                   args.cap_t,
                   args.lab_t,
                   args.im,
                   args.cap_im,
                   args.lab_im)

    # poetry run python src/latex_generator.py --t="table_data.xlsx" --cap_t="Example Table" --lab_t="tab:example" --im=kitty.jpg --cap_im="Example Image" --lab_im="fig:example"
