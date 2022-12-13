import essay_viewer.settings_utils as settings_utils


def test_with_url_prefix():
    assert "/" == settings_utils.with_url_prefix("", "")
    assert "/foo" == settings_utils.with_url_prefix("/", "foo")
    assert "/foo/bar" == settings_utils.with_url_prefix("/foo ", " bar")
    assert "/foo/bar" == settings_utils.with_url_prefix("foo", "   bar   ")
    assert "/foo/bar/" == settings_utils.with_url_prefix("foo/", "bar/")
    assert "/foo/bar/" == settings_utils.with_url_prefix("/foo/", "bar/")
