// Palettes: 'default', 'harmony light', 'soft pastel', 'pastel', 'bright', 'soft', 'ocean', 'vintage', 'vintage_desktop-dark', 'violet'

/*
"default":["#5F8B95","#BA4D51","#AF8A53","#955F71","#859666","#7E688C"],
"harmony light":["#FCB65E","#679EC5","#AD79CE","#A6C567","#E18E92","#DDED6E","#B7ABEA","#A8E7E3"],
"soft pastel":["#7CBAB4","#92C7E2","#75B5D6","#B78C9B","#F2CA84","#A7CA74"],
pastel:["#bb7862","#a4d5c2","#bb626a","#057d85","#a12135","#f5e7c9","#153459","#b1d2c6"],
bright:["#70c92f","#f8ca00","#e97f02","#bd1550","#800969","#7e4452","#9ab57e","#36a3a6"],
soft:["#ebdd8f","#9ab57e","#e55253","#7e4452","#e8c267","#565077","#6babac","#7e4452"],
ocean:["#75c099","#cff499","#378a8a","#a5dda5","#064970","#38c5d2","#00a7c6","#a2cefb"],
vintage:["#ebb192","#f2d1b5","#cb715e","#eb9692","#a85c4c","#f2c0b5","#f6ead7","#dd956c"],
"vintage_desktop-dark":["#e4a58b","#edc4a8","#be7060","#e48e8b","#9d5f51","#edb2a8","#f3e3cb","#dd956c"],
violet:["#d1a1d1","#f5ccdb","#7b5685","#7e7cad","#55263f","#5b41ab","#d9d3d9","#689cc1"]
*/

$(document).ready(function () {

	//////////////////////////////////////////////////////////////	
  if(document.getElementById("boysNamesChartContainer") != null) {			
		$("#boysNamesChartContainer").dxChart({
			title: {text: "Most Popular Boys Names"},
			dataSource: boysNamesChartDataSource,
			commonSeriesSettings: {argumentField: "name", type: "bar"},
			rotated: true,
			series: {name: "Names", valueField: "total", label: {visible: false} },
			tooltip: {enabled: true, font: {size: 16}},
			legend: {visible: false},
//			argumentAxis: {label: {font: {size: 11}}}
//  	  valueAxis: {label: {format: "thousands"}}
		});
	}
	
	//////////////////////////////////////////////////////////////	
  if(document.getElementById("girlsNamesChartContainer") != null) {			
		$("#girlsNamesChartContainer").dxChart({
			title: {text: "Most Popular Girls Names"},
			dataSource: girlsNamesChartDataSource,
			commonSeriesSettings: {argumentField: "name", type: "bar"},
			rotated: true,
			series: {name: "Names", valueField: "total", color: "#8B0000", label: {visible: false} },
			tooltip: {enabled: true, font: {size: 16}},
			legend: {visible: false},
//  	  valueAxis: {label: {format: "thousands"}}
		});
	}
			
	//////////////////////////////////////////////////////////////	
  if(document.getElementById("surnamesChartContainer") != null) {			
		$("#surnamesChartContainer").dxChart({
			title: {text: "Most Popular Surnames"},
			dataSource: surnamesChartDataSource,
			commonSeriesSettings: {argumentField: "name", type: "bar"},
			rotated: true,
			palette: "Soft Pastel",
			series: {name: "Names", valueField: "total", label: {visible: false} },
			tooltip: {enabled: true, font: {size: 16}},
			legend: {visible: false},
		});
  }
  
	//////////////////////////////////////////////////////////////
  if(document.getElementById("totRecordsChartContainer") != null) {			
		totRecordChartDataSource[0]["group"] = "Individuals";
		totRecordChartDataSource[1]["group"] = "Claims";
		totRecordChartDataSource[2]["group"] = "Documented Claims";
		totRecordChartDataSource[3]["group"] = "Impossible Claims";
		totRecordChartDataSource[4]["group"] = "Sources";

		$("#totRecordsChartContainer").dxChart({
		 title: {text: "Total Records Processed"},
		 dataSource: totRecordChartDataSource,
		 palette: "Soft Pastel",
		 commonSeriesSettings: {argumentField: "group", type: "bar"},
		 rotated: true,
		 series: {name: "Groups", valueField: "total", label: {visible: true} },
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}},
		 legend: {visible: false},
		 valueAxis: {label: {format: "millions"}}
		});
	}
		
	//////////////////////////////////////////////////////////////
  if(document.getElementById("expandedTotRecordsChartContainer") != null) {			
		expandedTotRecordChartDataSource[0]["group"]  = "Individuals";
		expandedTotRecordChartDataSource[1]["group"]  = "Family";
		expandedTotRecordChartDataSource[2]["group"]  = "Sources";
		expandedTotRecordChartDataSource[3]["group"]  = "Repositories";
		expandedTotRecordChartDataSource[4]["group"]  = "Notes";
		expandedTotRecordChartDataSource[5]["group"]  = "Claims";
		expandedTotRecordChartDataSource[6]["group"]  = "Documented Claims";
		expandedTotRecordChartDataSource[7]["group"]  = "Impossible Claims";
		expandedTotRecordChartDataSource[8]["group"]  = "Locations";
		expandedTotRecordChartDataSource[9]["group"]  = "Photos";
		expandedTotRecordChartDataSource[10]["group"] = "External URLs";
		expandedTotRecordChartDataSource[11]["group"] = "Immigrants";
		expandedTotRecordChartDataSource[12]["group"] = "Nobility Titles";

		$("#expandedTotRecordsChartContainer").dxChart({
		 title: {text: "Total Records Processed"},
		 dataSource: expandedTotRecordChartDataSource,
		 palette: "Soft Pastel",
		 commonSeriesSettings: {argumentField: "group", type: "bar"},
		 rotated: true,
		 series: {name: "Groups", valueField: "total", label: {visible: true} },
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}},
		 legend: {visible: false},
		});
	}
	
	//////////////////////////////////////////////////////////////	
  if(document.getElementById("avgRecordsChartContainer") != null) {			
		avgRecordsChartDataSource[0]["group"] = "Individuals";
		avgRecordsChartDataSource[1]["group"] = "Claims";
		avgRecordsChartDataSource[2]["group"] = "Documented Claims";
		avgRecordsChartDataSource[3]["group"] = "Impossible Claims";
		avgRecordsChartDataSource[4]["group"] = "Sources";

		$("#avgRecordsChartContainer").dxChart({
		 title: {text: "Average Records Per Database"},
		 dataSource: avgRecordsChartDataSource,
		 commonSeriesSettings: {argumentField: "group", type: "bar"},
		 rotated: true,
		 series: {name: "Groups", valueField: "total", label: {visible: true} },
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}},
		 legend: {visible: false},
		 valueAxis: {label: {format: "thousands"}}
		});
	}
						  
	//////////////////////////////////////////////////////////////	
  if(document.getElementById("distOfClaimsChartContainer") != null) {			
		distOfClaimsChartDataSource[0]["category"] = "Parents";
		distOfClaimsChartDataSource[1]["category"] = "Relationships";
		distOfClaimsChartDataSource[2]["category"] = "Names";
		distOfClaimsChartDataSource[3]["category"] = "Census";
		distOfClaimsChartDataSource[4]["category"] = "Vital Events";
		distOfClaimsChartDataSource[5]["category"] = "Other Events";
		distOfClaimsChartDataSource[6]["category"] = "Attributes";

		$("#distOfClaimsChartContainer").dxPieChart({
		 title: {text: "Distribution of Claims"},
		 dataSource: distOfClaimsChartDataSource,
		 series: {type: "doughnut",
							argumentField: "category",
							valueField: "value", 
							label: {visible: true,
											font: {size: 14},
											percentPrecision: 2,
											connector: {visible: true, width: 0.5},
											position: "columns",
											customizeText: function(arg) {return arg.valueText + " ( " + arg.percentText + ")";}
							},
		 },
		 tooltip: {enabled: true, percentPrecision: 2,	customizeText: function () {return this.argumentText;}},
		 legend: {horizontalAlignment: "center",	verticalAlignment: "bottom", itemTextPosition: "bottom", equalColumnWidth:true}
		});
  }

	//////////////////////////////////////////////////////////////	
  if(document.getElementById("docClaimsChartContainer") != null) {			
		docClaimsChartDataSource[0]["category"] = "Parents";
		docClaimsChartDataSource[1]["category"] = "Relationships";
		docClaimsChartDataSource[2]["category"] = "Names";
		docClaimsChartDataSource[3]["category"] = "Census";
		docClaimsChartDataSource[4]["category"] = "Vital Events";
		docClaimsChartDataSource[5]["category"] = "Other Events";
		docClaimsChartDataSource[6]["category"] = "Attributes";

		$("#docClaimsChartContainer").dxChart({
		 title: {text: "Number of Claims Documented"},
		 dataSource: docClaimsChartDataSource,
		 commonSeriesSettings: {argumentField: "category", type: "bar"},
		 commonAxisSettings:   {grid: {visible: true}},
		 commonPaneSettings:   {border:{visible: true, bottom: false}},
		 series: [{name: "Total Claims",	valueField: "total"},{name: "Documented Claims",	valueField: "documented"}],
		 legend: {horizontalAlignment: "center", verticalAlignment: "bottom", itemTextPosition: "right",},
		 tooltip: {enabled: true, shared: true, percentPrecision: 2, font: {size: 16}},
		});
	}

	//////////////////////////////////////////////////////////////	
  if(document.getElementById("avgLifeSpanChartContainer") != null) {			
		$("#avgLifeSpanChartContainer").dxChart({
		 title: {text: "Average Life Spans by Gender"},
		 dataSource: avgLifeSpanChartDataSource,
		 commonSeriesSettings: {argumentField: "year"},
		 commonAxisSettings:   {grid: {visible: true}},
		 commonPaneSettings:   {border:{visible: true, bottom: false}},
		 panes: [{name: "topPane"}, {name: "bottomPane"}],
		 series: [{pane: "topPane",    name: "Men",	          valueField: "men",     type: "spline"},
							{pane: "bottomPane", name: "Men Counted",	  valueField: "count_m", type: "bar"},
							{pane: "topPane",    name: "Women",	        valueField: "women",   type: "spline"},
							{pane: "bottomPane", name: "Women Counted", valueField: "count_w", type: "bar"}],
		 legend: {horizontalAlignment: "center", verticalAlignment: "bottom", itemTextPosition: "right",},
		 tooltip: {enabled: true, shared: true, percentPrecision: 2, font: {size: 16}},
		 valueAxis: [{pane: "topPane",    grid: {visible: true},  title: {text: "Average Life Span"}},
								 {pane: "bottomPane", grid: {visible: true }, title: {text: "Persons Counted"}}]
		});
	}
		
	//////////////////////////////////////////////////////////////	
  if(document.getElementById("avgAgesChartContainer") != null) {			
		avgAgesChartDataSource[0]["group"] = "First Marriage (Men)";
		avgAgesChartDataSource[1]["group"] = "First Marriage (Women)";
		avgAgesChartDataSource[2]["group"] = "Years Per Generation (All)";

		$("#avgAgesChartContainer").dxChart({
		 title: {text: "Average Ages by Group"},
		 dataSource: avgAgesChartDataSource,
		 palette: "Soft Pastel",
		 commonSeriesSettings: {argumentField: "group", type: "bar"},
		 rotated: true,
		 series: {name: "Groups", valueField: "age", label: {visible: true, customizeText: function(arg) {return arg.valueText + "y";}} },
	   valueAxis: {grid: {visible: false}, label: {visible: false}},
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}},
		 legend: {visible: false}
		});
	}
	
	//////////////////////////////////////////////////////////////	
  if(document.getElementById("xfactorChartContainer") != null) {			
		$("#xfactorChartContainer").dxChart({
		 title: {text: "Claim Type vs. Documentation Quality"},
		 dataSource: xfactorChartDataSource,
		 commonSeriesSettings: {argumentField: "claim", type: "fullstackedbar", selectionStyle: {hatching: {direction: "left"}} },
		 rotated: true,
		 pointSelectionMode: "multiple",
		 series: [
		   {name: "No Documentation",valueField: "none",    color: "#D33737"},
		   {name: "Average Quality", valueField: "average", color: "#FDD147"},
		   {name: "Good Quality",    valueField: "good",    color: "#5FA267"},
		   {name: "Best Quality",    valueField: "best",    color: "#5F88C5"},
		 ],
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}, customizeText: function () {return this.percentText + " (" + this.valueText + ")";}},
		 legend: {verticalAlignment: "bottom", horizontalAlignment: "center"},
//	   valueAxis: {grid: {visible: false}, label: {visible: false}},
	   pointClick: function(point) { point.isSelected() ? point.clearSelection() : point.select(); }		 
		});
	}

	//////////////////////////////////////////////////////////////
  if(document.getElementById("xfactorTotRecordsChartContainer") != null) {			
		xfactorTotRecordChartDataSource[0]["group"] = "Sources";
		xfactorTotRecordChartDataSource[1]["group"] = "Source Quality";
		xfactorTotRecordChartDataSource[2]["group"] = "Citations";
		xfactorTotRecordChartDataSource[3]["group"] = "Notes";
		xfactorTotRecordChartDataSource[4]["group"] = "Source References";
		xfactorTotRecordChartDataSource[5]["group"] = "Documented Claims";
		xfactorTotRecordChartDataSource[6]["group"] = "Parental Claims";
		xfactorTotRecordChartDataSource[7]["group"] = "Vital Claims";
		xfactorTotRecordChartDataSource[8]["group"] = "Impossible Claims";

		$("#xfactorTotRecordsChartContainer").dxChart({
		 title: {text: "Scores"},
		 dataSource: xfactorTotRecordChartDataSource,
		 commonSeriesSettings: {argumentField: "group", type: "bar"},
		 rotated: true,
		 series: {name: "Groups", valueField: "score", color: "#D8733B", label: {visible: true, format: 'fixedPoint', precision: 0, customizeText: function () {return this.valueText + " out of 100"}} },
	   valueAxis: {grid: {visible: false}, label: {visible: false}},
		 legend: {visible: false},
		});
	}

	if(document.getElementById("xfactorStatsChartContainer") != null) {
	  $("#xfactorStatsChartContainer").dxChart({
	   title: {text: "Top X X-Factors"},
	   series: {type: "bar", color: "#5F88C5", selectionStyle: {color: "#D33737",	hatching: "none"}, label: {visible: true}},
	   rotated: true,
	   legend: {visible: false},
	   tooltip: {enabled: false},
	   valueAxis: {grid: {visible: false}, label: {visible: false}},
		}); 
  }
	
	//////////////////////////////////////////////////////////////
  if(document.getElementById("expandedTotRecordsChartContainer2") != null) {			
		expandedTotRecordChartDataSource2[0]["group"]  = "Individuals";
		expandedTotRecordChartDataSource2[1]["group"]  = "Families";
		expandedTotRecordChartDataSource2[2]["group"]  = "Repositories";
		expandedTotRecordChartDataSource2[3]["group"]  = "Sources";
		expandedTotRecordChartDataSource2[4]["group"]  = "Notes";
		expandedTotRecordChartDataSource2[5]["group"]  = "Locations";

		expandedTotRecordChartDataSource2[6]["group"]  = "Source Citations";
		expandedTotRecordChartDataSource2[7]["group"]  = "Source References";
		expandedTotRecordChartDataSource2[8]["group"]  = "Note References";

		expandedTotRecordChartDataSource2[9]["group"]  = "Claims";
		expandedTotRecordChartDataSource2[10]["group"] = "Documented Claims";
		expandedTotRecordChartDataSource2[11]["group"] = "Impossible Claims";
		expandedTotRecordChartDataSource2[12]["group"] = "Census";
		expandedTotRecordChartDataSource2[13]["group"] = "Photos";
		expandedTotRecordChartDataSource2[14]["group"] = "External URLs";
		expandedTotRecordChartDataSource2[15]["group"] = "Immigrants";
		expandedTotRecordChartDataSource2[16]["group"] = "Nobility Titles";

		$("#expandedTotRecordsChartContainer2").dxChart({
		 title: {text: "Total Records Processed"},
		 dataSource: expandedTotRecordChartDataSource2,
		 palette: "Soft Pastel",
		 commonSeriesSettings: {argumentField: "group", type: "bar"},
		 rotated: true,
		 series: {name: "Groups", valueField: "total", label: {visible: true} },
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}},
		 legend: {visible: false},
		});
	}

});
