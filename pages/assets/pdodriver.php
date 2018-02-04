<?php if (array_search(__FILE__, get_included_files()) === 0) {die("<h4>Hackers! Be gone!</h4>");} ?>

<?php

if (!function_exists('dump_r')) 
{
	function dump_r($var=null)
	{
		echo("<pre>");
		if (!empty($var))	{
			print_r($var);
		}	else	{
			echo "[Empty, Null or 0]";
		}
		echo("</pre>");
	}
}

if (!function_exists('die_r')) 
{
	function die_r($var=null, $full = FALSE)
	{
		dump_r($var);
		$trace = debug_backtrace();
		if ($full)	{
			dump_r($trace);
		}	else  {
			foreach ($trace as $t)	{
				dump_r((isset($t['class']) ? $t['class'] . "::" : "") . $t['function'] . ": " . substr($t['file'], strrpos($t['file'], '/') + 1) . "[" . $t['line'] . "]");
			}
		}
		die();
	}	
}
	
class PDODriver
{
	public static function access_pdo_db($db_name)
	{
		try
		{
			// connect to the database
			$dbh = new PDO('sqlite:'.$db_name);
			if (!empty($dbh))
			{
				$dbh->exec("PRAGMA synchronous=OFF;");
				$dbh->exec("PRAGMA temp_store=MEMORY;");
				$dbh->exec("PRAGMA journal_mode=DELETE;");
				$dbh->exec("PRAGMA page_size=4096;");
				$dbh->exec("PRAGMA cache_size=10000;");
				
				$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
			
				return $dbh;
			}	
		}		
		catch (PDOException $e)
		{
			return false; // database not found
		}
		
		return false;
	}	

	// Check if a table exists in the current database.
	public static function table_exists($pdo, $table) 
	{
		// Try a select statement against the table
		// Run it in try/catch in case PDO is in ERRMODE_EXCEPTION.
		try {
			$result = $pdo->query("SELECT 1 FROM ".$table." LIMIT 1");
		} catch (Exception $e) {
			return FALSE; // table not found
		}

		// Result is either boolean FALSE (no table found) or PDOStatement Object (table found)
		return $result !== FALSE;
	}


	public static function exception($e,$text='')
	{
		$trace = $e->getTrace();

		$result = 'Exception: "';
		$result .= $e->getMessage();
		$result .= '" Trace: ';
		foreach($trace as $t)
		{
			if (isset($t['class']) && ($t['class'] != ''))
			{
				$result .= $t['class'];
				$result .= '::';
			}
			if (isset($t['function']) && ($t['function'] != ''))
			{
				$result .= $t['function'];
				$result .= '(); ';
			}
		}
		if (!empty($text))
		{
			$text = preg_replace("/[\n\r]/","",$text);
			$result .= '[Note: ' . $text . ']';
		}

		return $result;
	}

	public static function getMeta($db_name)
	{
		$result = array();
			
		$pdo = PDODriver::access_pdo_db($db_name);
		if (!empty($pdo) && PDODriver::table_exists($pdo, 'meta'))
		{		
			$sql = 'SELECT * FROM meta LIMIT 1';

			try
			{
				$statement = $pdo->prepare($sql);
				$statement->execute();
				$result = $statement->fetch();
				$success = true;
			}
			catch (PDOException $e)
			{
				$exception = PDODriver::exception($e,$sql);
				die_r($exception);
			}	
		}
		
		return $result;
	}	
	
	public static function getPage($db_name,$path)
	{
		$result = array();
			
		if (!empty($path))
		{
			$pdo = PDODriver::access_pdo_db($db_name);
			if (!empty($pdo) && PDODriver::table_exists($pdo, 'pages'))
			{		
				$sql = 'SELECT * FROM pages WHERE path = :path LIMIT 1';

				try
				{
					$statement = $pdo->prepare($sql);
					$statement->bindParam(":path", $path);
					$statement->execute();
					$result = $statement->fetch();
					$success = true;
				}
				catch (PDOException $e)
				{
					$exception = PDODriver::exception($e,$sql);
					die_r($exception);
				}	
			}
		}
		
		return $result;
	}	
}
