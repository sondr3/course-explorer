# courses-explorer

## What?

Me and a friend talked briefly about creating a graph of courses at UiB, which
courses depend on what and so on. This is a small attempt at doing this
automatically using Python.

## How

Use Nix or NixOS, run `nix shell` and `scrapy crawl courses -o courses.jl`. This
is a kind of JSON file where each line is a single JSON object. Do this because
of performance, it is faster to just append without having to read a JSON file
and append to a list. And furthermore, the Scrapy guide recommends using it for
when you have large datasets. Though >1Mb might not qualify.

To convert back into regular ol' JSON, install `jq` and run `jq -s . courses.jl > courses.json`.

## License

MIT.
