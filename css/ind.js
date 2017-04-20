// We load the latest version of d3.js from the Web.
require.config({paths: {d3: "https://d3js.org/d3.v3.min"}});
require(["d3"], function(d3) {

    // Parameter declaration, the height and width of our viz.
    var width = 300,
        height = 300;

    // Colour scale for node colours.
    var color = d3.scale.category10();

    // We create a force-directed dynamic graph layout.
    // D3 has number of layouts - refer to the documentation.
    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    // We select the < div> we created earlier and add an 
    // SVG = Scalable Vector Graphics
    var svg = d3.select("#d3-container").select("svg")
    if (svg.empty()) {
        svg = d3.select("#d3-container").append("svg")
                    .attr("width", width)
                    .attr("height", height);
    }

    // We load the JSON network file.
    d3.json("graph.json", function(error, graph) {
        // Within this block, the network has been loaded
        // and stored in the 'graph' object.

        // We load the nodes and links into the force-directed
        // graph and initialise the dynamics.
        force.nodes(graph.nodes)
            .links(graph.links)
            .start();

        // We create a < line> SVG element for each link
        // in the graph.
        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link");

        // We create a < circle> SVG element for each node
        // in the graph, and we specify a few attributes.
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 5)  // radius
            .style("fill", function(d) {
                // We colour the node depending on the degree.
                return color(d.degree); 
            })
            .call(force.drag);
			
		node.on('dblclick', connectedNodes);


        // The label each node its node number from the networkx graph.
        node.append("title")
            .text(function(d) { return d.id; });
		
		// The label each node its node number from the networkx graph.
		node.append("title")
			.text(function(d) { return "Node: " + d.id + "\n" + "Degree: " + d.degree + "\n" + "Katz: " + d.katz;});



        // We bind the positions of the SVG elements
        // to the positions of the dynamic force-directed graph,
        // at each time step.
        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });
    });
});


//Toggle stores whether the highlighting is on
var toggle = 0;

//Create an array logging what is connected to what
var linkedByIndex = {};

for (var i = 0; i < graph.nodes.length; i++) {
    linkedByIndex[i + "," + i] = 1;
};

graph.links.forEach(function (d) {
    linkedByIndex[d.source.index + "," + d.target.index] = 1;
});

//Looks up whether a pair of nodes are neighbours.
function neighboring(a, b) {
    return linkedByIndex[a.index + "," + b.index];
}

function connectedNodes() {
    if (toggle == 0) {
        //Reduce the opacity of all but the neighbouring nodes to 0.3.
        var d = d3.select(this).node().__data__;
        node.style("opacity", function (o) {
            return neighboring(d, o) | neighboring(o, d) ? 1 : 0.3;
        });
        //Reduce the opacity of all but the neighbouring edges to 0.8.
        link.style("opacity", function (o) {
            return d.index==o.source.index | d.index==o.target.index ? 1 : 0.8;
        });
        //Increases the stroke width of the neighbouring edges.
        link.style("stroke-width", function (o) {
            return d.index==o.source.index | d.index==o.target.index ? 3 : 0.8;
        });
        //Reset the toggle.
        toggle = 1;
    } else {
        //Restore everything back to normal
        node.style("opacity", 1);
        link.style("opacity", 1);
        link.style("stroke-width", 1);
        toggle = 0;
    }
}