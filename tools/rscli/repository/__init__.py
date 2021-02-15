import json
from os import makedirs, listdir
from os.path import join, exists
from typing import List
from shutil import rmtree
from .model import StationRepository, RepositoryBundle, RepositoryStation, WebRadioStream

def write_repository(repo: StationRepository, folder: str):
    if not exists(folder):
        makedirs(folder)
    if len(listdir(folder)) > 0:
        rmtree(folder)
    bundles_folder = join(folder, "bundles")
    if not exists(bundles_folder):
        makedirs(bundles_folder)
    for bundle in repo.bundles:
        bundle_path = join(bundles_folder, bundle.identifier()+".json")
        with open(bundle_path, "w") as file:
            json.dump(bundle.to_dict(), file)
    index_path = join(folder, "index.json")
    with open(index_path, "w") as file:
        json.dump(repo.to_dict(), file)

