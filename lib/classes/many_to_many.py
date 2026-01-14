class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        # title is immutable after set; validate on init
        self.title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # allow initial set only; ignore subsequent attempts to change
        if not hasattr(self, "_title"):
            if not isinstance(value, str):
                raise Exception("Title must be a string")
            if not (5 <= len(value) <= 50):
                raise Exception("Title must be between 5 and 50 characters")
            self._title = value
        else:
            # ignore attempts to change after initialization
            return
        
class Author:
    def __init__(self, name):
        # name is immutable after set; validate on init
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # allow initial setting, but ignore subsequent attempts to change
        if not hasattr(self, "_name"):
            if not isinstance(value, str):
                raise Exception("Author name must be a string")
            if len(value) <= 0:
                raise Exception("Author name must be longer than 0 characters")
            self._name = value
        else:
            # ignore attempts to change after initialization
            return

    def articles(self):
        # return list of Article instances written by this author
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        # unique list of Magazine instances this author has contributed to
        mags = []
        for article in self.articles():
            if article.magazine not in mags:
                mags.append(article.magazine)
        return mags

    def add_article(self, magazine, title):
        # create and return new Article associated with this author
        return Article(self, magazine, title)

    def topic_areas(self):
        areas = [mag.category for mag in self.magazines()]
        return list(dict.fromkeys(areas)) if areas else None

class Magazine:
    all = []

    def __init__(self, name, category):
        # name and category are mutable but validated
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # must be str and between 2 and 16 characters inclusive
        if not isinstance(value, str):
            # ignore invalid assignment
            if not hasattr(self, "_name"):
                raise Exception("Magazine name must be a string")
            return
        if not (2 <= len(value) <= 16):
            # ignore invalid assignment
            if not hasattr(self, "_name"):
                raise Exception("Magazine name must be between 2 and 16 characters")
            return
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # must be str and length > 0
        if not isinstance(value, str):
            if not hasattr(self, "_category"):
                raise Exception("Category must be a string")
            return
        if len(value) == 0:
            if not hasattr(self, "_category"):
                raise Exception("Category must be longer than 0 characters")
            return
        self._category = value

    def articles(self):
        # return list of Article instances published by this magazine
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # unique list of authors who have written for this magazine
        authors = []
        for article in self.articles():
            if article.author not in authors:
                authors.append(article.author)
        return authors

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        authors = self.contributors()
        if not authors:
            return None
        result = []
        for author in authors:
            count = sum(1 for a in self.articles() if a.author == author)
            if count > 2:
                result.append(author)
        return result if result else None

    @classmethod
    def top_publisher(cls):
        # return magazine with most articles
        if not Article.all:
            return None
        counts = {mag: len(mag.articles()) for mag in cls.all}
        if not counts:
            return None
        return max(counts, key=counts.get)