<?php
$start_time = microtime(true);
set_include_path('../');
include_once 'commons/config.php';
include_once 'commons/langs.php';
?>
	<!DOCTYPE html>
	<html lang="<?php echo($user_language); ?>">
	<head>
		<?php include 'commons/DOM/head.php'; ?>
		<title><?php print(localize('about.head.title')); ?></title>
		<meta name="description" content="<?php print(localize('about.head.description')); ?>">
		<meta property="og:title" content="<?php print(localize('about.og.title')); ?>"/>
		<meta property="og:type" content="website"/>
		<meta property="og:url" content="<?php echo($host_uri . l10n_url_abs('/')); ?>"/>
		<meta property="og:image" content="<?php echo($host_uri); ?>/resources/NibblePoker/images/logos/v2_opengraph.png"/>
		<meta property="og:image:type" content="image/png"/>
		<meta property="og:description" content="<?php print(localize('about.og.description')); ?>"/>
	</head>
	<body>
	<?php
	include_once 'commons/DOM/utils.php';
	$SIDEBAR_IDS = ['about'];
	include 'commons/DOM/sidebar.php';
	?>
	<header class="w-full p-m pl-s">
		<h1 class="t-size-17 t-w-500">
			<i class="fad fa-user t-size-16 mr-s t-muted"></i><?php print(localize("about.header.title")); ?>
		</h1>
		<?php include 'commons/DOM/header-lang.php'; ?>
	</header>
	<main id="main" class="rl-m border border-r-0 p-l">
		
		<?php printMainHeader(localize("about.topmost.title"), "fab fa-twitter", "@NibblePoker"); ?>
		<p class="m-s">
			<a href="https://twitter.com/messages/compose?recipient_id=937370791334895616" class="bland-link button-link">
				<button class="p-xs r-s border b-light primary"><?php print(localize("contact.twitter.compose")); ?></button>
			</a>
		</p>
		
		<div class="px-xxs">
			<?php printSubHeader(localize("about.education.title"), null, null); ?>
			
			<details>
				<summary>ABC</summary>
				DEF
			</details>
			
			<?php printSubHeader(localize("about.skills.title"), null, null); ?>
			
			<?php printSubHeader(localize("about.work.title"), null, null); ?>
		</div>
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