<?php
if (basename(__FILE__) == basename($_SERVER["SCRIPT_FILENAME"])) {
    header('HTTP/1.1 403 Forbidden');
    die();
}
defined('SIDEBAR_ID') or define('SIDEBAR_ID', 'default');
?>
<div class="sidebar">
	<div class="sidebar-menu font-weight-bold">
		<a href="<?php print(l10n_url_abs('/')); ?>" class="sidebar-brand no-select">
			<img id="logo-sidebar" src="/resources/Azias/logos/logov3-test-finalized.svg" alt="logo" draggable="false">
		</a>
		<h4 class="text-center quantum ucase font-size-28 text-muted">N<span class="text-super-muted">ibble</span> P<span class="text-super-muted">oker</span></h4>
		<div class="sidebar-divider"></div>
		<a id="sbl-home" href="<?php print(l10n_url_abs('/')); ?>" class="sidebar-link sidebar-link-with-icon<?php if(SIDEBAR_ID=="home"){echo(" active");} ?>">
			<span class="sidebar-icon"><i class="fad fa-home" aria-hidden="true"></i></span>
			<?php print(localize("home.title.nav")); ?>
		</a>
		<a id="sbl-blog" href="<?php print(l10n_url_abs('/blog/')); ?>" class="sidebar-link sidebar-link-with-icon<?php if(SIDEBAR_ID=="blog"){echo(" active");} ?>">
			<span class="sidebar-icon"><i class="fad fa-rss-square"></i></span>
			<?php print(localize("blog.title")); ?>
        </a>
		<div class="sidebar-divider"></div>
		<a id="sbl-programming" href="<?php print(l10n_url_abs('/programming/')); ?>" class="sidebar-link sidebar-link-with-icon">
			<span class="sidebar-icon"><i class="fad fa-code"></i></span>
			<?php print(localize("programming.title")); ?>
		</a>
		<div class="ml-20">
			<a id="sbl-purebasic" href="<?php print(l10n_url_abs('/programming/purebasic/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-microchip"></i></span>
				<?php print(localize("programming.purebasic.title")); ?>
			</a>
			<a id="sbl-python" href="<?php print(l10n_url_abs('/programming/python/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fab fa-python"></i></span>
				<?php print(localize("programming.python.title")); ?>
			</a>
			<!--<a id="sbl-others" href="<?php print(l10n_url_abs('/programming/others/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-ellipsis-h"></i></span>
				<?php print(localize("programming.others.title")); ?>
            </a>-->
			<a id="sbl-docker" href="<?php print(l10n_url_abs('/programming/docker/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fab fa-docker"></i></span>
				<?php print(localize("programming.docker.title")); ?>
			</a>
			<div class="sidebar-divider"></div>
			<a id="sbl-projects-apps" href="<?php print(l10n_url_abs('/programming/applications/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-browser"></i></span>
				<?php print(localize("programming.apps.title")); ?>
			</a>
			<a id="sbl-projects-tutorials" href="<?php print(l10n_url_abs('/programming/tutorials/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-books"></i></span>
				<?php print(localize("programming.tutorials.title")); ?>
			</a>
			<a id="sbl-projects-tools" href="<?php print(l10n_url_abs('/programming/tools/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-tools"></i></span>
				<?php print(localize("programming.tools.title")); ?>
			</a>
		</div>
		<!--<div class="sidebar-divider"></div>
		<a id="sbl-electronics" href="<?php print(l10n_url_abs('/electronics/')); ?>" class="sidebar-link sidebar-link-with-icon">
			<span class="sidebar-icon"><i class="fad fa-microchip"></i></span>
			<?php print(localize("electronics.title")); ?>
		</a>
		<div class="ml-20">
			<a id="sbl-iot" href="<?php print(l10n_url_abs('/electronics/iot/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-house-signal"></i></span>
				<?php print(localize("electronics.iot.title")); ?>
			</a>
			<a id="sbl-elec-misc" href="<?php print(l10n_url_abs('/electronics/experiments/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-flask"></i></span>
				<?php print(localize("electronics.experiments.title")); ?>
			</a>
			<a id="sbl-ham" href="<?php print(l10n_url_abs('/electronics/ham/')); ?>" class="sidebar-link sidebar-link-with-icon">
				<span class="sidebar-icon"><i class="fad fa-broadcast-tower"></i></span>
				<?php print(localize("electronics.ham.title")); ?>
			</a>
		</div>-->
		<div class="sidebar-divider"></div>
		<a id="sbl-links" href="<?php print(l10n_url_abs('/links/')); ?>" class="sidebar-link sidebar-link-with-icon<?php if(SIDEBAR_ID=="links"){echo(" active");} ?>">
			<span class="sidebar-icon"><i class="fad fa-link"></i></span>
			<?php print(localize("links.title")); ?>
		</a>
		<a id="sbl-about" href="<?php print(l10n_url_abs('/about/')); ?>" class="sidebar-link sidebar-link-with-icon<?php if(SIDEBAR_ID=="about"){echo(" active");} ?>">
			<span class="sidebar-icon"><i class="fad fa-user"></i></span>
			<?php print(localize("about.title")); ?>
		</a>
		<a id="sbl-contact" href="<?php print(l10n_url_abs('/contact/')); ?>" class="sidebar-link sidebar-link-with-icon<?php if(SIDEBAR_ID=="contact"){echo(" active");} ?>">
			<span class="sidebar-icon"><i class="fad fa-mailbox"></i></span>
			<?php print(localize("contact.title")); ?>
		</a>
	</div>
</div>
