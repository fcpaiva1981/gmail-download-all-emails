import json
import locale
from typing import Any

from dateutil import parser

from src.dto.FormatedDateDTO import FormatedDateDTO
from src.interfaces.IUtilsFunctions import IUtilsFunctions


class UtilsFunctions(IUtilsFunctions):

    def format_date(self, date: str) -> FormatedDateDTO:
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

        return FormatedDateDTO(date, pt_br_format, only_date, only_date_time)

    def json_serializer(self, obj) -> Any | None:
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return None

    def json_dmps(self, obj) -> str:
        return json.dumps(obj,
                          indent=4,
                          default=self.json_serializer,
                          ensure_ascii=False
                          )