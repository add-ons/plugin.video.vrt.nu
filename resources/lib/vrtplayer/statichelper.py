class StaticHelper:

    @staticmethod
    def format_image_url(element):
        raw_thumbnail = element.find("img")['srcset'].split('1x,')[0]
        return raw_thumbnail.replace("//", "https://")

    @staticmethod
    def minutes_string_to_seconds_int(minutes):
        try:
            return int(minutes) * 60
        except ValueError:
            return None
