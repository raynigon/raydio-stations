# raydio-stations
Source for the Bundle Repository

## Directory structure

- `data/` contains all the radio stations as json files
    - `global/` subcategory which contains all stations which cant be assigned to a specific country
    - `countries/` subcategory which contains a folder for each country
        - `de/` subcategory for germany in lower letters (see https://en.wikipedia.org/wiki/ISO_3166-1)
            - `br/` subcategory for a broadcasting corporation
            - `ndr/` subcategory for a broadcasting corporation
            - `wdr/` subcategory for a broadcasting corporation
            - ...
        - ...

## Contribute

1. You want to add a new Station
2. Fork the repository and checkout
3. Install all required packages for the `rscli` tool with `pip3 install -r tools/requirements.txt`
4. Start the `rscli` command line tool to create a new station 
    * 4.1. Run `python3 tools/rscli/main.py add-station`
    * 4.2. Enter all needed Informations
    * 4.3. Run `python3 tools/rscli/main.py validate` to check if your changes are valid
    * 4.4. Run `python3 tools/rscli/main.py check-streams` to check the given stream informations
5. Create a PR, all CI Pipelines should be green in order to accept your PR as fast as possible
6. We will merge your PR and you can refresh the stations in [rayd.io](https://rayd.io)

