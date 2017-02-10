<template>
	<ul class="pagination text-center" role="navigation" aria-label="Pagination">
		<li v-bind:class="['pagination-previous', current > 1 ? '' : 'disabled']">
			<a v-if="current > 1" v-link="{name: $route.name, params: {index: +current - 1}}">Previous</a>
			<template v-else>Previous</template>
</li>
		<li v-for="n in total" v-bind:class="[n + 1 == current ? 'current':'']">
			<template v-if="n+1 == current"><span class="show-for-sr">You're on page</span>{{n+1}}</template>
			<a v-else v-link="{name: $route.name, params: {index: n + 1}}">{{n+1}}</a>
		</li>

		<li v-bind:class="['pagination-next', current < total ? '' : 'disabled']">
			<a v-if="current < total" v-link="{name: $route.name, params: {index: +current + 1}}">Next</a>
			<template v-else>Next</template>
		</li>
	</ul>
</template>

<script>
export default {
	props: ['current', 'total']
}
</script>
