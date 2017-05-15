//data
	var label= ['','Web','Data Science','DevOps'];

	var people = [359,339,220];

	//////////////////////
	// Graph 1
	//////////////////////

	//color
	var colors = ['#FBBE3B'];

	var grid1 = d3.range(25).map(function(i){
		return {'x1':0,'y1':0,'x2':0,'y2':120};
	});

	var tickVals1 = grid1.map(function(d,i){
		if(i>0){ return i*50; }
		else if(i===0){ return "100";}
	});

	var xscale1 = d3.scale.linear()
					.domain([10,400]) //chart range
					.range([0,722]);

	var yscale1 = d3.scale.linear()
					.domain([0,label.length])
					.range([0,120]);

	var colorScale1 = d3.scale.quantize()
					.domain([0,label.length])
					.range(colors);

	var canvas1 = d3.select('#barchart1')
					.append('svg')
					.attr({'width':900,'height':180});

	var grids1 = canvas1.append('g')
					  .attr('id','grid1')
					  .attr('transform','translate(200,10)')
					  .selectAll('line')
					  .data(grid1)
					  .enter()
					  .append('line')
					  .attr({'x1':function(d,i){ return i*30; },
							 'y1':function(d){ return d.y1; },
							 'x2':function(d,i){ return i*30; },
							 'y2':function(d){ return d.y2; },
						})
					  .style({'stroke':'#adadad','stroke-width':'1px'});

	var	xAxis1 = d3.svg.axis();
		xAxis1
			.orient('bottom')
			.scale(xscale1)
			.tickValues(tickVals1);

	var	yAxis1 = d3.svg.axis();
		yAxis1
			.orient('left')
			.scale(yscale1)
			.tickSize(2)
			.tickFormat(function(d,i){ return label[i]; })
			.tickValues(d3.range(17));

	var y_xis1 = canvas1.append('g')
					  .attr("transform", "translate(200,0)")
					  .attr('id','yAxis1')
					  .call(yAxis1);

	var x_xis1 = canvas1.append('g')
					  .attr("transform", "translate(200,120)")
					  .attr('id','xAxis1')
					  .call(xAxis1);

	var chart1 = canvas1.append('g')
						.attr("transform", "translate(200,0)")
						.attr('id','bars')
						.selectAll('rect')
						.data(people)
						.enter()
						.append('rect')
						.attr('height',19)
						.attr({'x':0,'y':function(d,i){ return yscale1(i)+19; }})
						.style('fill',function(d,i){ return colorScale1(i); })
						.attr('width',function(d){ return 0; });


	var transit = d3.select("svg").selectAll("rect")
					    .data(people)
					    .transition()
					    .duration(1000)
					    .attr("width", function(d) {return xscale1(d); });

	var transitext = d3.select('#bars')
						.selectAll('text')
						.data(people)
						.enter()
						.append('text')
						.attr({'x':function(d) {return xscale1(d)-30; },'y':function(d,i){ return yscale1(i)+35; }})
						.text(function(d){ return d; }).style({'fill':'#fff','font-size':'14px'});
