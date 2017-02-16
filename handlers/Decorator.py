def _check_user_or_login(func):
    def check(self, *args, **kwargs):
        user = self.check_user()
        if not user:
            return self.redirect('/login')
        else:
            return_func = func(self, *args, **kwargs)
            return return_func
    return check


def _check_article_own(func):
    def check(self, article_key, *args, **kwargs):
        if not self.user_own_article(article_key):
            self.redirect('/view')
        else:
            return_func = func(self, article_key, *args, **kwargs)
            return return_func
    return check


def _check_comment_own(func):
    def check(self, comment_key, *args, **kwargs):
        if not self.user_own_comment:
            self.redirect('/view')
        else:
            return_func = func(self, comment_key, *args, **kwargs)
            return return_func
    return check
