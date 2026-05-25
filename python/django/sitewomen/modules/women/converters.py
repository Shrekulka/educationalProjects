# sitewomen/modules/women/converters.py


class FourDigitYearConverter:

    regex = r"[0-9]{4}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f"{value:04d}"