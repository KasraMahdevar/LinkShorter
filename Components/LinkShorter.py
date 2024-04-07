import random, string
from datetime import datetime, timedelta
from Models.DB_Links import DB_Links as table_links


class LinkShorter:

    def __init__(self, url, hostname, expire_after_days=30):
        self.old_url = url
        self.hostname = hostname
        self.new_url = None
        self.expire_days = expire_after_days

    def short_url(self, length_of_url=7):
        path = self.__generate_path(size=length_of_url)
        self.new_url = self.hostname + '/' + path
        entry = table_links.find_object_link(shorten_url=self.new_url)
        while entry != None:
            self.new_url = self.__generate_path(size=length_of_url)

        now = datetime.now()
        table_links.create_new_link(old_url=self.old_url, shorten_url=self.new_url,
                                    expire_date=now + timedelta(days=self.expire_days))

        return self.new_url

    def __generate_path(self, size):
        chars = string.ascii_uppercase + string.digits
        new_str = ''
        for _ in range(size):
            new_str = new_str + (random.choice(chars))
        return new_str
