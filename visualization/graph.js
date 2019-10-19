const height = 1000,
  width = 1000;

const svg = d3
  .select("svg")
  .attr("width", width)
  .attr("height", height)
  .call(
    d3.zoom().on("zoom", function() {
      svg.attr("transform", d3.event.transform);
    })
  )
  .append("g");

const data = d3.json("graph.json").then(graph => {
  console.log(graph);

  const simulation = d3
    .forceSimulation(graph.nodes)
    .force("charge", d3.forceManyBody())
    .force(
      "link",
      d3.forceLink(graph.links).id(d => {
        return d.id;
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
    .attr("r", 20)
    .style("fill", "#69b3a2");

  node.each(d => {
    d.degree = 0;
  });

  link.each(d => {
    d.source.degree += 1;
    d.target.degree += 1;
  });

  node.append("title").text(d => {
    return d.name;
  });

  node.attr("r", d => {
    const minRadius = 10;
    return minRadius + d.degree * 3;
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
});
