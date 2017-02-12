<template>
	<ul class="pagination text-center" role="navigation" aria-label="Pagination">
		<li v-bind:class="['pagination-previous', current > 1 ? '' : 'disabled']">
			<template v-if="current > 1">
				<router-link :to="{name: $route.name, params: {index: +current - 1}}">Previous</router-link>
			</template>
			<template v-else>Previous</template>
		</li>
		<li v-for="n in total" v-bind:class="[n == current ? 'current':'']">
			<template v-if="n == current"><span class="show-for-sr">You're on page</span>{{n}}</template>
			<template v-else>
				<router-link :to="{name: $route.name, params: {index: n}}">{{n}}</router-link>
			</template>
		</li>

		<li v-bind:class="['pagination-next', current < total ? '' : 'disabled']">
			<template v-if="current < total" >
				<router-link :to="{name: $route.name, params: {index: +current + 1}}">Next</router-link>
			</template>
			<template v-else>Next</template>
		</li>
	</ul>
</template>

<script>
export default {
	name: 'pagination',
	props: ['current', 'total']
}
</script>
