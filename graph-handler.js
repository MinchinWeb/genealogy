// Palettes: 'default', 'harmony light', 'soft pastel', 'pastel', 'bright', 'soft', 'ocean', 'vintage', 'vintage_desktop-dark', 'violet'

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
		 valueAxis: {label: {format: "millions"}}
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
		 tooltip: {enabled: true, percentPrecision: 2, font: {size: 16}},
		 legend: {visible: false}
		});
	}
	
});
