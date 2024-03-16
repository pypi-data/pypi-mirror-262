import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from utils import get_player_suffix
    from lookup import lookup
    from request_utils import get_wrapper, get_selenium_wrapper
except:
    from basketball_reference_scraper.utils import get_player_suffix
    from basketball_reference_scraper.request_utils import get_wrapper, get_selenium_wrapper
    from basketball_reference_scraper.lookup import lookup

def get_stats(_name, stat_type='PER_GAME', playoffs=False, career=False, ask_matches = True):
    name = lookup(_name, ask_matches)
    suffix = get_player_suffix(name)
    if not suffix:
        return pd.DataFrame()
    stat_type = stat_type.lower()
    table = None
    if stat_type in ['per_game', 'totals', 'advanced'] and not playoffs:
        r = get_wrapper(f'https://www.basketball-reference.com/{suffix}')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', { 'id': stat_type })
            table = str(table)
        else:
            raise ConnectionError('Request to basketball reference failed')
    elif stat_type in ['per_minute', 'per_poss'] or playoffs:
        if playoffs:
            xpath = f"//table[@id='playoffs_{stat_type}']"
        else:
            xpath = f"//table[@id='{stat_type}']"
        table = get_selenium_wrapper(f'https://www.basketball-reference.com/{suffix}', xpath)
    if table is None:
        return pd.DataFrame()
    df = pd.read_html(table)[0]
    df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS', 'Awards': 'AWARDS'}, inplace=True)
    if 'FG.1' in df.columns:
        df.rename(columns={'FG.1': 'FG%'}, inplace=True)
    if 'eFG' in df.columns:
        df.rename(columns={'eFG': 'eFG%'}, inplace=True)
    if 'FT.1' in df.columns:
        df.rename(columns={'FT.1': 'FT%'}, inplace=True)

    career_index = df[df['SEASON']=='Career'].index[0]
    if career:
        df = df.iloc[career_index+2:, :]
    else:
        df = df.iloc[:career_index, :]

    df = df.reset_index().drop('index', axis=1)
    return df


def get_game_logs(_name, year, playoffs=False, ask_matches=True):
    name = lookup(_name, ask_matches)
    suffix = get_player_suffix(name).replace('.html', '')
    if playoffs:
        selector = 'pgl_basic_playoffs'
        url = f'https://www.basketball-reference.com/{suffix}/gamelog-playoffs'
    else:
        selector = 'pgl_basic'
        url = f'https://www.basketball-reference.com/{suffix}/gamelog/{year}'
    r = get_wrapper(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', { 'id': selector })
        df = pd.read_html(str(table))[0]
        df.rename(columns = {'Date': 'DATE', 'Age': 'AGE', 'Tm': 'TEAM', 'Unnamed: 5': 'HOME/AWAY', 'Opp': 'OPPONENT',
            'Unnamed: 7': 'RESULT', 'GmSc': 'GAME_SCORE', 'Series': 'SERIES' }, inplace=True)
        df['HOME/AWAY'] = df['HOME/AWAY'].apply(lambda x: 'AWAY' if x=='@' else 'HOME')
        df = df[df['Rk']!='Rk']
        df = df.drop(['Rk', 'G'], axis=1).reset_index(drop=True)
        if not playoffs:
            df['DATE'] = pd.to_datetime(df['DATE'])
        return df
    else:
        raise ConnectionError('Request to basketball reference failed')

def get_player_headshot(_name, ask_matches=True):
    name = lookup(_name, ask_matches)
    suffix = get_player_suffix(name)
    jpg = suffix.split('/')[-1].replace('html', 'jpg')
    url = 'https://d2cwpp38twqe55.cloudfront.net/req/202006192/images/players/'+jpg
    return url

def get_player_splits(_name, season_end_year, stat_type='PER_GAME', ask_matches=True):
    name = lookup(_name, ask_matches)
    suffix = get_player_suffix(name)[:-5]
    r = get_wrapper(f'https://www.basketball-reference.com/{suffix}/splits/{season_end_year}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if table:
            df = pd.read_html(str(table))[0]
            for i in range(1, len(df['Unnamed: 0_level_0','Split'])):
                if isinstance(df['Unnamed: 0_level_0','Split'][i], float):
                    df['Unnamed: 0_level_0','Split'][i] = df['Unnamed: 0_level_0','Split'][i-1]
            df = df[~df['Unnamed: 1_level_0','Value'].str.contains('Total|Value')]
            
            headers = df.iloc[:,:2]
            headers = headers.droplevel(0, axis=1)
                
            if stat_type.lower() in ['per_game', 'shooting', 'advanced', 'totals']:
                if stat_type.lower() == 'per_game':
                    df = df['Per Game']
                    df['Split'] = headers['Split']
                    df['Value'] = headers['Value']
                    cols = df.columns.tolist()
                    cols = cols[-2:] + cols[:-2]
                    df = df[cols]
                    return df
                elif stat_type.lower() == 'shooting':
                    df = df['Shooting']
                    df['Split'] = headers['Split']
                    df['Value'] = headers['Value']
                    cols = df.columns.tolist()
                    cols = cols[-2:] + cols[:-2]
                    df = df[cols]
                    return df
                
                elif stat_type.lower() == 'advanced':
                    df =  df['Advanced']
                    df['Split'] = headers['Split']
                    df['Value'] = headers['Value']
                    cols = df.columns.tolist()
                    cols = cols[-2:] + cols[:-2]
                    df = df[cols]
                    return df
                elif stat_type.lower() == 'totals':
                    df = df['Totals']
                    df['Split'] = headers['Split']
                    df['Value'] = headers['Value']
                    cols = df.columns.tolist()
                    cols = cols[-2:] + cols[:-2]
                    df = df[cols]
                    return df
            else:
                raise Exception('The "stat_type" you entered does not exist. The following options are: PER_GAME, SHOOTING, ADVANCED, TOTALS')
    else:
        raise ConnectionError('Request to basketball reference failed')