<?php
// Making sure the file is included and not accessed directly.
if(basename(__FILE__) == basename($_SERVER["SCRIPT_FILENAME"])) {
	header('HTTP/1.1 403 Forbidden'); die();
}

$host = "nibblepoker.lu";
$host_uri = "https://nibblepoker.lu";
$dir_commons = dirname(__FILE__);
$dir_root = realpath($dir_commons . "/../");
$dir_content = realpath($dir_commons . "/../" . "content/");
?>