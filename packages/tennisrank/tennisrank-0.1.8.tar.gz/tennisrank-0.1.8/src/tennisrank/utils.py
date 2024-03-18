import difflib
import pandas as pd

from tennisrank.model import Player, Match, PlayerRank, Surface
from tennisrank.cache import Cache


def df_to_matches(df: pd.DataFrame):
    df['win_weight'] = 1.0
    for _, row in df.iterrows():
        winner = Player(id=row['winner_id'], name=row['winner_name'])
        loser = Player(id=row['loser_id'], name=row['loser_name'])
        surface = Surface.HARD if pd.isna(
            row['surface']) else Surface[row['surface'].upper()]
        win_weight = row['win_weight']
        yield Match(winner=winner, loser=loser, win_weight=win_weight, surface=surface)


def ranks_to_df(ranks: list[PlayerRank]) -> pd.DataFrame:
    dicts = [
        {
            'player_id': r.player.id, 'player_name': r.player.name,
            'rank': r.rank, 'surface': r.surface.name.title()
        }
        for r in ranks
    ]
    return pd.DataFrame(dicts)


def fuzzy_match(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def load_matches_from_url(url: str):
    def iter_matches():
        df = pd.read_csv(url)
        yield from df_to_matches(df)

    return list(iter_matches())


def load_matches_from_github(association: str, year: int) -> str:
    if association.lower() == 'atp':
        url = (
            'https://raw.githubusercontent.com/JeffSackmann/'
            f'tennis_atp/master/atp_matches_{year}.csv'
        )
        return load_matches_from_url(url)
    elif association.lower() == 'wta':
        url = (
            'https://raw.githubusercontent.com/JeffSackmann/'
            f'tennis_atp/master/atp_matches_{year}.csv'
        )
        return load_matches_from_url(url)
    else:
        raise ValueError(f'Unsupported association: {association}')


def load_matches(association: str, *years: int) -> list[Match]:
    cache = Cache()

    def iter_matches():
        for year in years:
            cached = cache.read(association, year)
            if cached is not None:
                yield from cached
            else:
                # load from url
                matches = load_matches_from_github(association, year)
                # write to cache
                cache.write(association, year, matches)
                yield from matches

    return list(iter_matches())


def load_atp(*years):
    return load_matches('atp', *years)


def load_wta(*years):
    return load_matches('wta', *years)
