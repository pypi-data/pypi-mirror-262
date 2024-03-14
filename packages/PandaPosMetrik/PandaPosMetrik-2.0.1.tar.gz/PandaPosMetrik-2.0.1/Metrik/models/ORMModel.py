from .OrmManager import OrmManager
from typing import get_type_hints, get_args
import datetime

class Model(object):
    objects = OrmManager()
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        hints = get_type_hints(self)
        # Sonra tarih tipindekileri dönüştürün
        for key, hint_type in hints.items():
            if hint_type == datetime.datetime:
                attr_value = getattr(self, key, None)  # Varsayılan olarak None dön
                if attr_value and isinstance(attr_value, str):  # Değer string ve atanmışsa
                    try:
                        # Tarih formatı kontrolü ve dönüştürme
                        setattr(self, key, datetime.datetime.fromisoformat(attr_value))
                    except ValueError:
                        # Geçersiz tarih formatı, uygun bir hata yönetimi ekleyin
                        pass
            
