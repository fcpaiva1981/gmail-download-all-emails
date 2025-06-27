import locale
from dateutil import parser


def format_date(date: str):
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        print("Locale 'pt_BR.UTF-8' not found!. Trying 'Portuguese_Brazil'.")
        try:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
        except locale.Error:
            print("Locale to 'Português do Brasil' not found in system. Trying 'Portuguese_Brazil'.")


    now = parser.parse(date)

    pt_br_format = now.strftime("%A, %d de %B de %Y")
    only_date = now.strftime("%Y-%m-%d")
    only_date_time = now.strftime("%Y-%m-%d_%H%M%S")

    return [now, pt_br_format, only_date, only_date_time]
