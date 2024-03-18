from datetime import datetime
import os
import pickle

import appdirs

from tennisrank.model import Match

ONE_DAY_IN_SECS = 60*60*24


class Cache:

    def __init__(self, app='TennisRank', author='Kefaloukos Technologies ApS', ttl_secs=ONE_DAY_IN_SECS):
        super().__init__()
        self.ttl_secs = ttl_secs
        self.cache_dir = appdirs.user_cache_dir(app, author)
        self.init_cache_dir()

    def init_cache_dir(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def read(self, association: str, year: int) -> list[Match]:
        file_path = self.get_file_path(association, year)
        if os.path.exists(file_path):
            modification_epoch = os.path.getmtime(file_path)
            modification_ts = datetime.fromtimestamp(modification_epoch)
            if (datetime.now() - modification_ts).total_seconds() < self.ttl_secs:
                with open(file_path, 'rb') as fin:  # Use 'rb' to read in binary mode
                    matches = pickle.load(fin)
                    self._check_matches(matches)
                    return matches

    def write(self, association: str, year: int, matches: list[Match]):
        self._check_matches(matches)
        file_path = self.get_file_path(association, year)
        # Use the highest protocol available
        with open(file_path, 'wb') as fout:
            pickle.dump(matches, fout, protocol=pickle.HIGHEST_PROTOCOL)

    def get_file_path(self, association: str, year: int):
        return f'{self.cache_dir}/{association.lower()}_{year}.trm'

    def _check_matches(self, matches: list[Match]):
        for match in matches:
            assert isinstance(
                match, Match), 'match was not an instance of match'
