<template>
<div>
	<div class="row">
		<div class="small-12 columns">
			<div class="text-right">
				<span class="current">{{progress}}</span>/<span class="count">{{total}}</span>
			</div>
		</div>
	</div>
	<div class="row">
		<div class="small-12 columns">
			<div class="progress" role="progressbar" tabindex="0" v-bind:aria-valuenow="progress" aria-valuemin="0" v-bind:aria-valuetext="progress / total * 100 + 'percent'" v-bind:aria-valuemax="total">
				<div class="progress-meter" v-bind:style="{width: progress / total * 100 + '%'}"></div>
			</div>
		</div>
	</div>
</div>
</template>

<style>
.current {
	font-size: 200%;
}
</style>

<script>
export default {
	name: 'progress',
	props: {
		total: {
			type: Number,
			required: true
		},
		progress: {
			type: Number,
			required: true
		}
	}
}
</script>
