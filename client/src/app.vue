<template>
<div>
	<div class="top-bar">
		<div class="top-bar-title">
			<h1><a ui-sref="home">Interview</a><small>beta</small></h1>
		</div>
	</div>
	<router-view></router-view>
</div>
</template>

<script>
export default {
	name: 'app'
}
</script>
