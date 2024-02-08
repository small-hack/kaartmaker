# Kaartmaker
Make world and regional labeled maps based on voting. Most commonly used for representing UN General Assembly votes.

![Map of world Ukraine votes](./examples/world_UNGA_vote_on_ceasefire_in_Ukraine.png)

![Map of world Gaza votes](./examples/world_UNGA_vote_on_ceasefire_in_Gaza.png)


Maps (sovereignty, units, subunits, and disputed areas) downloaded from:
https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-details/

### Secondary features

- You can do download geojson files with the [download_geojson.sh](./download_geojson.sh) script in this repo.

- generate geojson files for specific regions :)

- Colors are colorblind friendly, selected from: https://davidmathlogic.com/colorblind

## How To

To use `kaartmaker`, you'll need to provide a CSV file with columns called `NAME_EN` and `VOTE`. Valid votes are `YES`|`NO` or `AGAINST`|`ABSTENTION`|`IN FAVOR` Example when documenting :

```csv
NAME_EN,VOTE
Brazil,IN FAVOR
Czechia,AGAINST
Germany,ABSTENTION
```

# status
Mostly stable, but happy to take a look at Issues and Pull Requests :)
