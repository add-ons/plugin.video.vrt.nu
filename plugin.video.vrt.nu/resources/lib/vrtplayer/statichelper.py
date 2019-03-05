def replace_newlines_and_strip(text):
    return text.replace('\n', '').strip()


def replace_double_slashes_with_https(url):
    return url.replace('//', 'https://')
