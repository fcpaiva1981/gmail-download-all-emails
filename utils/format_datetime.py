import locale
from dateutil import parser


def formatDate(date: str):
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        print("Locale 'pt_BR.UTF-8' not found!. Trying 'Portuguese_Brazil'.")
        try:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
        except locale.Error:
            print("Locale to 'Português do Brasil' not found in system. Trying 'Portuguese_Brazil'.")


    now = parser.parse(date)

    ptBrFormat = now.strftime("%A, %d de %B de %Y")
    onlyDate = now.strftime("%Y-%m-%d")

    return [now, ptBrFormat, onlyDate]
