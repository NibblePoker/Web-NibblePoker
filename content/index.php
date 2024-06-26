<?php
$start_time = microtime(true);

// Importing required scripts.
set_include_path('../');
include_once 'commons/config.php';
include_once 'commons/langs.php';

// Preparing the content
include_once 'commons/content/manager.php';
include_once 'commons/content/composer.php';
$contentManager = ContentManager::createContentManager($config_dir_content);
$content = NULL;
if(!$contentManager->hasError && $contentManager->displayType == EContentDisplayType::DISPLAY) {
	$content = load_content_by_file_path($contentManager->contentFilepath);
	if(is_null($content)) {
		$contentManager->hasError = true;
		$contentManager->errorMessageKey = "content.error.message.cannot.load";
	}
}
$content_error_message = localize($contentManager->errorMessageKey);

// Checking if an error occurred while loading data and parsing the URL.
// And if not, enabling special features.
$content_error_code = 200;
if($contentManager->hasError) {
	// TODO: Add condition for the lack of data for an item.
	if(is_null($contentManager->rootIndexEntries)) {
		// Failed to get a display type or to extract types.
		header("HTTP/1.1 400 Bad Request");
		$content_error_code = 400;
	} else {
		//Other error. (No article, ...)
		header("HTTP/1.1 500 Internal Server Error");
		$content_error_code = 500;
	}
} else {
	$enable_code_highlight = true;
	$enable_gallery = true;
}
?>
<!DOCTYPE html>
<html lang="<?php echo($user_language); ?>">
<head>
	<?php
	// Remark: The 'glider' and 'highlight.js' stylesheets are included here.
	include 'commons/DOM/head.php';
	
	$content_head_image = $host_uri . "/resources/NibblePoker/images/logos/v2_opengraph.png";
	$content_head_image_type = "image/png";
	
    // Preparing values for the head's tags.
    if ($contentManager->hasError) {
		$content_head_title = localize("content.error.head.title");
		$content_head_description = $content_error_message;
		$content_head_og_title = localize("content.error.og.title");
		$content_head_og_description = $content_error_message;
    } elseif($contentManager->displayType == EContentDisplayType::DISPLAY) {
		$content_head_title =
			localize("content.item.head.title.prefix") .
            $content->get_head_title() .
			localize("content.item.head.title.suffix");
		$content_head_description = $content->get_head_description();
	    $content_head_og_title =
			localize("content.item.og.title.prefix") .
			$content->get_head_title() .
			localize("content.item.og.title.suffix");
		$content_head_og_description = $content->get_head_description();
	    
	    if(!is_null($content->metadata->opengraph->image)) {
		    $content_head_image = $host_uri . $content->metadata->opengraph->image;
	    }
		
	    if(!is_null($content->metadata->opengraph->image_type)) {
		    $content_head_image_type = $content->metadata->opengraph->image_type;
	    } else {
			switch(pathinfo($content_head_image, PATHINFO_EXTENSION)) {
				case "png":
					$content_head_image_type = "image/png";
					break;
				case "jpg":
				case "jpeg":
					$content_head_image_type = "image/jpeg";
					break;
				case "gif":
					$content_head_image_type = "image/gif";
					break;
				case "svg":
					$content_head_image_type = "image/svg+xml";
					break;
				case "webp":
					$content_head_image_type = "image/webp";
					break;
				case "apng":
					$content_head_image_type = "image/apng";
					break;
			}
	    }
    } elseif($contentManager->displayType == EContentDisplayType::SEARCH) {
		$content_head_title = localize("content.search.head.title");
		$content_head_description = localize("content.search.head.description");
		$content_head_og_title = localize("content.search.og.title");
		$content_head_og_description = localize("content.search.og.description");
    }
    
    // TODO: Fix the OG URL tag to add the tags !
	?>
    <title><?php echo($content_head_title); ?></title>
    <meta name="description" content="<?php echo($content_head_description); ?>">
    <meta property="og:title" content="<?php echo($content_head_og_title); ?>"/>
    <meta property="og:type" content="website"/>
    <meta property="og:url" content="<?php echo($host_uri . l10n_url_abs('/')); ?>"/>
    <meta property="og:image" content="<?php echo($content_head_image); ?>"/>
    <meta property="og:image:type" content="<?php echo($content_head_image_type); ?>"/>
    <meta property="og:description" content="<?php echo($content_head_og_description); ?>"/>
</head>
<body class="layout-generic">
<?php
include_once 'commons/DOM/utils.php';
$SIDEBAR_IDS = array_merge(['content'], is_null($contentManager->requestedTags) ? [] : $contentManager->requestedTags);
include 'commons/DOM/sidebar.php';
?>
<header class="w-full p-m pl-s">
    <h1 class="t-size-17 t-w-500">
        <?php
		if($contentManager->hasError) {
			echo('<i class="fad fa-exclamation-triangle t-size-16 mr-s t-muted"></i>');
			echo(localize("content.header.base"));
			echo('<span class="mobile-hide">');
			echo('<span class="mx-s t-size-15">❱</span>');
			echo(localize("content.error.header"));
			echo('</span>');
		} elseif($contentManager->displayType == EContentDisplayType::SEARCH) {
			echo('<i class="fad fa-briefcase t-size-16 mr-s t-muted"></i>');
			echo(localize("content.header.base"));
			echo('<span class="mobile-hide">');
			echo('<span class="mx-s t-size-15">❱</span>');
			echo(localize("content.search.header"));
			echo('</span>');
		} elseif($contentManager->displayType == EContentDisplayType::DISPLAY) {
			echo('<i class="fad fa-briefcase t-size-16 mr-s t-muted"></i>');
		    echo(localize("content.header.base"));
			echo('<span class="mobile-hide">');
			echo('<span class="mx-s t-size-15">❱</span>');
            echo('<span class="t-size-16">' . $content->get_head_title() . '</span>');
			echo('</span>');
		}
		?>
    </h1>
	<?php include 'commons/DOM/header-lang.php'; ?>
</header>
<main id="main" class="rl-m border border-r-0 p-l">
	<?php
	// Checking if an error occurred.
    if($content_error_code != 200) {
		if($contentManager->displayType == EContentDisplayType::SEARCH) {
			printMainHeader(localize("content.error.heading.main.search"), "fad fa-exclamation-triangle");
		} elseif($contentManager->displayType == EContentDisplayType::DISPLAY) {
			printMainHeader(localize("content.error.heading.main.content"), "fad fa-exclamation-triangle");
		} else {
			printMainHeader(localize("content.error.heading.main.fallback"), "fad fa-exclamation-triangle");
        }
        
        echo('<h3 class="mt-m t-size-18 t-center content-error-text mx-auto">' . $content_error_message . '</h3>');
        
        goto content_printing_end;
    }
    
	if($contentManager->displayType == EContentDisplayType::SEARCH) {
        // We are handling a content search with at least one result.
        
        // Making the header with the amount of results.
		printMainHeader(
			count($contentManager->rootIndexEntries) > 1 ?
				localize("content.search.heading.main.multiple") :
				localize("content.search.heading.main.single"),
            "fad fa-file-search",
			count($contentManager->rootIndexEntries) . " " . (
			count($contentManager->rootIndexEntries) > 1 ?
				localize("content.search.count.multiple") :
				localize("content.search.count.single")));
        
        // Printing the entry for each piece of relevant content.
        $doPrintRuler = false;
		foreach($contentManager->rootIndexEntries as $current_content) {
			/** @var ContentIndexEntry $current_content */
			
            if($doPrintRuler) {
				echo('<hr class="subtle">');
            } else {
				$doPrintRuler = true;
            }
            
			echo('<div class="p-s">');
			echo('<a class="casper-link" href="'.l10n_url_abs("/content/".$current_content->id).'">');
			echo('<div class="content-search-entry">');
   
            echo('<img class="content-search-image mr-s r-l" src="' . $current_content->image . '">');
            echo('<h3 class="mb-xs">' . $current_content->title[$user_language] . '</h3>');
            echo('<p>' . $current_content->preamble[$user_language] . '</p>');
   
			echo('</div>');
			echo('</a>');
			
            echo('<p class="mt-xs"><i class="fad fa-tags t-size-8"></i>');
            foreach($current_content->tags as $current_content_tag) {
                echo('<a href="' . l10n_url_abs("/content/?tags=".$current_content_tag) .
                    '" class="ml-xs">#' . $current_content_tag . '</a>');
			}
            echo('</p>');
   
			echo('</div>');
		}
        
        // TODO: Print the tags used in the search and others that may be available.
	} elseif($contentManager->displayType == EContentDisplayType::DISPLAY) {
		// Printing the content
        echo($content->get_html());
	}
 
	// Label used when there is an error to skip the content printing parts.
	content_printing_end:
	?>
</main>
<?php
include 'commons/DOM/footer.php';
include 'commons/DOM/scripts.php';
?>
</body>
</html>
<?php
$end_time = microtime(true);
if($print_execution_timer) {
	echo("<!-- PHP execution took " . round(($end_time - $start_time) * 1000, 2) . " ms -->");
}
?>