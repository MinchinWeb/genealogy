$.fn.textWidth = function(text="", font="") {
	if (!$.fn.textWidth.fakeEl) {
		$.fn.textWidth.fakeEl = $('<span>').hide().appendTo(document.body);
	}
	$.fn.textWidth.fakeEl.text(text || this.val() || this.text()).css('font', font || this.css('font'));
	return $.fn.textWidth.fakeEl.width();
};

function printBarChart(obj, bindingId, rgbcolor, padPush, fontSize, fontName, rankT) {
	
	var X = [];
	var inner = [];
	inner.push("x", "value");
	X.push(inner);
    $.each( obj, function( key, value ) {
		var inner = [];
        inner.push(key, parseFloat(value)); 
		X.push(inner);
    });

	var pad = 0;
	X.forEach(function(data) {
		var w = $.fn.textWidth(data[0], fontSize+"px "+fontName);
		if (w > pad) {
			pad = w;
		}
	});
	pad += padPush;
		
	var chart = c3.generate({
		bindto: '#'+bindingId,
		data: {
			x: 'x',
			rows: X,
			type : 'bar',
		},
        axis: {
            rotated: true,
			x: {
                type: 'category',
				tick: {
					multiline: false
				},				
            },
			y: {
				show: false,
			},
		},
		bar: {
			width: {
				ratio: 0.6 
			},
		},
		color: {
			pattern: ['#'+rgbcolor]
		},
		tooltip: {
			contents: function(d, defaultTitleFormat, defaultValueFormat, color) {
				var $$ = this;
				var config = $$.config;
				var CLASS = $$.CLASS;
				var text, i, title, bgcolor;

				for (i = 0; i < d.length; i++) {
					if (! (d[i] && (d[i].value || d[i].value === 0))) { continue; }
					if (! text) {
						title = rankT+' #'+(d[i].index+1);
						text = "<table class='" + CLASS.tooltip + "'>" + (title || title === 0 ? "<tr><th colspan='2'>" + title + "</th></tr>" : "");
					}

					bgcolor = $$.levelColor ? $$.levelColor(d[i].value) : color(d[i].id);

					var dName = X[d[i].index+1][0];
					
					text += "<tr class='" + CLASS.tooltipName + "-" + d[i].id + "'>";
					text += "<td class='name'><span style='background-color:" + bgcolor + "'></span>" + dName + "</td>";
					text += "<td class='left'>" + d[i].value + "</td>";
					text += "</tr>";
				}

				return text + "</table>";   
			},
		},
		legend: {show: false},	
		padding: {left: pad},		
	});

	$('.c3 text').css('font-size', fontSize+"px");
}

function printComboChart(obj, bindingId, yearT, menT, menCountedT, womenT, womenCountedT, avgLifeSpanT, numCountedT) {
	var X = [];
	var inner = [];
	// there appears to be an issue with splines using variables as names
	inner.push(yearT, "Men", menCountedT, "Women", womenCountedT);
	X.push(inner);
    $.each( obj, function( key, value ) {
		var inner = [];
        inner.push(parseFloat(value[0]), parseFloat(value[1]), parseFloat(value[2]), parseFloat(value[3]), parseFloat(value[4])); 
		X.push(inner);
    });
	
	var chart = c3.generate({
		bindto: '#'+bindingId,
		data: {
			x: yearT,
			rows: X,
			type: 'bar',
			types: {
				"Men" : 'spline',
				"Women" : 'spline',
			},
			axes: {
				"Men" : 'y2',
				menCountedT : 'y',
				"Women" : 'y2',
				womenCountedT : 'y',
			},
		},
		bar: {
			width: {
				ratio: 0.5
			}
		},	
		axis: {
			x: {
				tick: {
					culling: false
				}				
			},				
			y2: {
				show: true,
				label: {
					text: avgLifeSpanT,
					position: 'outer-middle'
				}
			},			
			y: {
				show: true,
				label: {
					text: numCountedT,
					position: 'outer-middle'
				}
			}
		},		
	});	
}

function printBoysNames(obj,rankT) {
    printBarChart(obj, 'boysNamesChartContainer', '1f77b4', 15, 15, 'Open Sans', rankT);
}

function printGirlsNames(obj,rankT) {
    printBarChart(obj, 'girlsNamesChartContainer', 'ffbb78', 15, 15, 'Open Sans', rankT);
}

function printSurnames(obj,rankT) {
    printBarChart(obj, 'surnamesChartContainer', '98df8a', 15, 15, 'Open Sans', rankT);
}

function printLifeSpans(obj, yearT, menT, menCountedT, womenT, womenCountedT, avgLifeSpanT, numCountedT) {
    printComboChart(obj, 'avgLifeSpanChartContainer', yearT, menT, menCountedT, womenT, womenCountedT, avgLifeSpanT, numCountedT);
}