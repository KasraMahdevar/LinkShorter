from Models.DB_Links import DB_Links as table_links
from datetime import datetime


class LoadURL:

    def __init__(self, url):
        self.shorten_url = url
        self.old_url = None

    def load(self):
        entry = table_links.find_object_link(self.shorten_url)
        if entry == None:
            return 'not found'
        elif entry.expire_date <= datetime.now():
            table_links.delete_object_link(shorten_url=self.shorten_url)
            return 'expired'
        else:
            return entry.old_url