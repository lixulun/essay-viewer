def with_url_prefix(url_prefix, appender):
    prepared_prefix = url_prefix.strip()
    if (not prepared_prefix) or prepared_prefix == "/":
        prepared_prefix = "/"
    else:
        prepared_prefix = "/" + prepared_prefix.strip("/") + "/"
    return prepared_prefix + appender.strip()
