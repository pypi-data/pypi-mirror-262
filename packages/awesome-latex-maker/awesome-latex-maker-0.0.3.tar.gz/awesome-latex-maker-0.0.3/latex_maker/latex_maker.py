from io import StringIO
from pdflatex import PDFLaTeX
from typing import List, Any, Iterable


def create_table(data: List[List[Any]]) -> str:
    """Table generation function for the first task"""

    width = max(len(row) for row in data)
    height = len(data)

    expression = StringIO()

    # prefix
    expression.write(f'\\begin{{tabular}}{{ |{" ".join(["c"]*width)}| }}\n\t\\hline\n')

    # body
    for row in data:
        expression.write(f'\t{" & ".join(str(el) for el in row)} \\\\\n')

    # suffix
    expression.write(f'\t\\hline\n\\end{{tabular}}\n')

    return expression.getvalue()


def create_image(image_path: str) -> str:
    """Image generation function for the second task"""

    return f'\\includegraphics{{{image_path}}}\n'


def build_document(expressions: Iterable[str]) -> str:
    """Document generation function"""

    expression_doc = StringIO()

    # prefix
    expression_doc.write('\\documentclass{article}\n\\usepackage{graphicx}\n\n\\begin{document}\n\n')

    for exp in expressions:
        expression_doc.write(exp)
        expression_doc.write('\n')

    # suffix
    expression_doc.write('\\end{document}\n')

    return expression_doc.getvalue()


def output_document(latex_code: str, pdf_name: str):
    PDFLaTeX.from_binarystring(
        latex_code.encode('utf-8'),
        pdf_name
    ).create_pdf(
        keep_pdf_file=True,
        keep_log_file=False
    )
