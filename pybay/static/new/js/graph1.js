//data
	var label2= ['','Student','Individual Contributer','Contributes to Open Source', 'Open to Job Opportunities', 'Working Professional', 'Leadership Experience', 'Presented at Conferences','Presented at Conferences'];

	var people2 = [36,145,111,141,394,145,123,58];
	//////////////////////
	// Graph 2
	//////////////////////

	//color
	var colors2 = ['#0000b4'];

	var grid2 = d3.range(25).map(function(i){
		return {'x1':0,'y1':0,'x2':0,'y2':320};
	});

	var tickVals2 = grid2.map(function(d,i){
		if(i>0){ return i*50; }
		else if(i===0){ return "100";}
	});

	var xscale2 = d3.scale.linear()
					.domain([10,425]) //chart range
					.range([0,722]);

	var yscale2 = d3.scale.linear()
					.domain([0,label2.length])
					.range([0,320]);

	var colorscale2 = d3.scale.quantize()
					.domain([0,label2.length])
					.range(colors2);

	var canvas2 = d3.select('#barchart2')
					.append('svg')
					.attr({'width':900,'height':480});

	var grids2 = canvas2.append('g')
					  .attr('id','grid2')
					  .attr('transform','translate(150,10)')
					  .selectAll('line')
					  .data(grid2)
					  .enter()
					  .append('line')
					  .attr({'x1':function(d,i){ return i*30; },
							 'y1':function(d){ return d.y1; },
							 'x2':function(d,i){ return i*30; },
							 'y2':function(d){ return d.y2; },
						})
					  .style({'stroke':'#adadad','stroke-width':'1px'});

	var	xAxis2 = d3.svg.axis();
		xAxis2
			.orient('bottom')
			.scale(xscale2)
			.tickValues(tickVals2);

	var	yAxis2 = d3.svg.axis();
		yAxis2
			.orient('left')
			.scale(yscale2)
			.tickSize(2)
			.tickFormat(function(d,i){ return label2[i]; })
			.tickValues(d3.range(17));

	var y_xis2 = canvas2.append('g')
					  .attr("transform", "translate(150,0)")
					  .attr('id','yAxis2')
					  .call(yAxis2);

	var x_xis2 = canvas2.append('g')
					  .attr("transform", "translate(150,320)")
					  .attr('id','xAxis2')
					  .call(xAxis2);

	var chart2 = canvas2.append('g')
						.attr("transform", "translate(150,0)")
						.attr('id','bars')
						.selectAll('rect')
						.data(people2)
						.enter()
						.append('rect')
						.attr('height',19)
						.attr({'x':0,'y':function(d,i){ return yscale2(i)+19; }})
						.style('fill',function(d,i){ return colorscale2(i); })
						.attr('width',function(d){ return 0; });


	var transit2 = d3.select("svg").selectAll("rect")
					    .data(people2)
					    .transition()
					    .duration(1000)
					    .attr("width", function(d) {return xscale2(d); });

	var transitext2 = d3.select('#bars')
						.selectAll('text')
						.data(people2)
						.enter()
						.append('text')
						.attr({'x':function(d) {return xscale2(d)-30; },'y':function(d,i){ return yscale2(i)+35; }})
						.text(function(d){ return d; }).style({'fill':'#fff','font-size':'14px'});
