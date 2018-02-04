<?php

	include('includes.php');	// defines GIGATREES_PAGES_DB (written by Gigatrees)
	include('pdodriver.php');	// PDO functions to access the sqlite database

	$gigatrees_debug = false;
	
	// get server names
	$gigatrees_path = $_SERVER['REQUEST_URI'];		
	
	$gigatrees_self = $_SERVER['PHP_SELF'];
	$gigatrees_root = str_replace('router.php','',$gigatrees_self);
	
	preg_match('%^(.*?)[\\\\/]*(([^/\\\\]*?)(\.([^\.\\\\/]+?)|))[\\\\/\.]*$%im', $gigatrees_path, $gigatrees_m);
		if($gigatrees_m[1]) $gigatrees_routes['dirname']   = $gigatrees_m[1];
		if($gigatrees_m[3]) $gigatrees_routes['filename']  = $gigatrees_m[3];

	// rebuild the path
	$gigatrees_path = '';

	// normalize directory name
	$gigatrees_routes['dirname'] = ltrim($gigatrees_routes['dirname'],"/");
	
	if (!empty($gigatrees_routes['dirname']))	
	{
		// strip the domain root from the directory name
		$gigatrees_path = str_replace(ltrim(rtrim($gigatrees_root,"/"),"/"),"",$gigatrees_routes['dirname']);
	}
	
	// normalize resulting path
	$gigatrees_path = ltrim($gigatrees_path,"/");

	// force root
	if ($gigatrees_path == $gigatrees_routes['dirname'])
	{
		$gigatrees_path = "";
	}
	else
	{
		// append filename unless it is index
		if (!empty($gigatrees_routes['filename']) && ($gigatrees_routes['filename'] != "index"))
		{
			// append a slash if needed
			if (!empty($gigatrees_path) && (substr($gigatrees_path, -1) != "/"))
			{
				$gigatrees_path .= "/";
			}
			
			// append the filename
			$gigatrees_path .= $gigatrees_routes['filename'];	
		}
	}

	// database requires a slash, so prepend it
	$gigatrees_path = '/' . $gigatrees_path;
	
	// get the page	(path should have a preceding slash)
	$gigatrees_result = PDODriver::getPage(GIGATREES_PAGES_DB,$gigatrees_path);
	if (!empty($gigatrees_result)) 
	{
		$gigatrees_header = "";
		$gigatrees_footer = "";
	
		// get the meta macros
		$gigatrees_meta = PDODriver::getMeta(GIGATREES_PAGES_DB);
		if (!empty($gigatrees_meta)) 
		{
			if (!empty($gigatrees_meta['header'])) $gigatrees_header = $gigatrees_meta['header'];
			if (!empty($gigatrees_meta['footer'])) $gigatrees_footer = $gigatrees_meta['footer'];
			
			// decode the macros
			$gigatrees_data = json_decode($gigatrees_meta['data']);
			if (!empty($gigatrees_data))
			{
				if (!empty($gigatrees_data->macros))
				{
					// clean the header and footer
					foreach ($gigatrees_data->macros as $key => $value)
					{
						if (!empty($gigatrees_header)) $gigatrees_header = str_replace($key,$value,$gigatrees_header);
						if (!empty($gigatrees_footer)) $gigatrees_footer = str_replace($key,$value,$gigatrees_footer);
					}
				}
			}
		}		
		
		// get the page macros
		if (!empty($gigatrees_result['data']))
		{
			// decode the macros
			$gigatrees_data = json_decode($gigatrees_result['data']);
			if (!empty($gigatrees_data->macros))
			{
				// clean the header and footer
				foreach ($gigatrees_data->macros as $key => $value)
				{
					if (!empty($gigatrees_header)) $gigatrees_header = str_replace($key,$value,$gigatrees_header);
					if (!empty($gigatrees_footer)) $gigatrees_footer = str_replace($key,$value,$gigatrees_footer);
				}
			}
		}

		if (!empty($gigatrees_header)) $gigatrees_header = str_replace("%DomainRoot%",$gigatrees_root,$gigatrees_header);
		if (!empty($gigatrees_footer)) $gigatrees_footer = str_replace("%DomainRoot%",$gigatrees_root,$gigatrees_footer);
		
		// Fix body relative links
		if (!empty($gigatrees_result['html'])) $gigatrees_body = $gigatrees_result['html'];
		if (!empty($gigatrees_body))           $gigatrees_body = str_replace("%DomainRoot%",$gigatrees_root,$gigatrees_body);
		
		// display the page
		echo($gigatrees_header.$gigatrees_body.$gigatrees_footer);
	}
	else if ($gigatrees_debug)
	{
		dump_r($gigatrees_self);	
		dump_r($gigatrees_root);	
		dump_r($gigatrees_routes);	
		dump_r($gigatrees_path);	
		dump_r($gigatrees_result);	
		die_r($_SERVER);	
	}
	else // page not found
	{	
		// inform the browser
		if (function_exists('http_response_code')) 
		{
			http_response_code(404);
		}
		
		// redirect to the home page
		header('Location: '.$_SERVER['REQUEST_SCHEME'].'://'.$_SERVER['HTTP_HOST']); 
		exit;
	}
