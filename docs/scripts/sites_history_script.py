from pathlib import Path

import pandas
import pydriller
from git import Repo
import io

repo_path = Path(__file__).parent.parent.parent
site_data = repo_path / "docs" / "_data" / "sites.csv"
repo = Repo(str(repo_path))
df = None


def get_change_hashes():
    for commit in pydriller.RepositoryMining(str(repo_path), filepath='docs/_data/sites.csv').traverse_commits():
        yield commit.hash, commit.author_date


for hash, date in get_change_hashes():
    commit = repo.commit(hash)
    try:
        target_file = commit.tree / "docs" / "_data" / "sites.csv"
    except KeyError:
        continue
    with io.BytesIO(target_file.data_stream.read()) as f:
        new_df = pandas.read_csv(f)
        new_df['date'] = date
        if df is None:
            df = new_df
        else:
            df = pandas.concat([df, new_df])

df.to_csv("ranking_history.csv")
