import re


class EmailFilter:

    @staticmethod
    def filter_name(text):
        pattern_between_gls = "<[^>]+>"
        pattern_between_ocb = "\([^\)]+\)"
        text = re.sub(pattern_between_gls, "", text)
        text = re.sub(pattern_between_ocb, "", text)
        text = text.replace("\"", "")
        text = text.rstrip()
        return text

    @staticmethod
    def filter_email_from(text):
        pattern_between_gls = "<(.*?)>"
        search = re.search(pattern_between_gls, text)
        if search is not None:
            text = search.group(1)
        return text

    @staticmethod
    def filter_subject(text):
        text = text.replace('\r', '').replace('\n', '')
        return text
