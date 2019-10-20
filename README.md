# courses-explorer

## What?

Me and a friend talked briefly about creating a graph of courses at UiB, which
courses depend on what and so on. This is a small attempt at doing this
automatically using Python.

## How

Most everything is done automatically, to find all the institutes and faculties
at UiB run `scrapy crawl faculties -o faculties.jl`. Then, to get the courses
themselves run `scrapy crawl courses -o courses.jl`; Finally, to actually build
the graph and everything run `python d3json.py` and it'll create a `graph.json`
file. You can now start the development server with `npm run dev` (though you
should probably run `npm i` first) and view the exploding graph.

## License

MIT.
