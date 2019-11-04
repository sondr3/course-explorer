const height = 1200,
  width = 1200;
let GRAPH = null;

const makeGraph = (selector, graph) => {
  console.log(graph);
  const svg = d3
    .select(selector)
    .attr("width", "95vw")
    .attr("height", "95vh")
    .call(
      d3.zoom().on("zoom", function() {
        svg.attr("transform", d3.event.transform);
      })
    )
    .append("g");

  const simulation = d3
    .forceSimulation(graph.nodes)
    .force("charge", d3.forceManyBody())
    .force(
      "link",
      d3.forceLink(graph.links).id(d => {
        return d.id;
      })
    )
    .force(
      "collide",
      d3.forceCollide().radius(d => {
        return d.degree + 15 * 3.5;
      })
    )
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg
    .append("g")
    .attr("class", "link")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .style("stroke", "#696969");

  const node = svg
    .append("g")
    .attr("class", "node")
    .selectAll("circle")
    .data(graph.nodes)
    .enter()
    .append("circle")
    .attr("r", d => d.degree)
    .style("fill", "#69b3a2")
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );

  node.append("title").text(d => {
    return d.name;
  });

  node.attr("r", d => {
    const minRadius = 15;
    return minRadius + d.degree * 5;
  });

  simulation.nodes(graph.nodes).on("tick", ticked);
  simulation.force("link").links(graph.links);

  function ticked() {
    link
      .attr("x1", d => {
        return d.source.x;
      })
      .attr("y1", d => {
        return d.source.y;
      })
      .attr("x2", d => {
        return d.target.x;
      })
      .attr("y2", d => {
        return d.target.y;
      });

    node
      .attr("cx", d => {
        return d.x;
      })
      .attr("cy", d => {
        return d.y;
      });
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
};

const fetchGraph = async () => {
  try {
    const resp = await fetch("graph.json");
    return await resp.json();
  } catch (err) {
    return console.error(err);
  }
};

const filterGraph = graph => {
  let filtered = graph.nodes.filter(node => node.degree > 0);
  return { nodes: filtered, links: graph.links };
};

fetchGraph("graph.json").then(graph => {
  GRAPH = graph;
  makeGraph("svg", filterGraph(graph));
});

const filterButton = document.getElementById("filter-button");
let filtered = true;
filterButton.addEventListener("click", () => {
  if (filtered) {
    filterButton.innerText = "Hide unconnected courses";
    d3.select("svg")
      .selectAll("*")
      .remove();
    makeGraph("svg", GRAPH);
  } else {
    filterButton.innerText = "Show all courses";
    d3.select("svg")
      .selectAll("*")
      .remove();
    makeGraph("svg", filterGraph(GRAPH));
  }
  filtered = !filtered;
});
