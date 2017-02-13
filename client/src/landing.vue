<template>
<div class="cover">
	<div class="row">
		<div class="small-12 columns">
			<h2>New interview</h2>
			<form v-on:submit.prevent="createInterview">
				<div class="input-group">
					<fieldset>
						<legend>Applicant</legend>
						<input type="text" class="input-group-field" v-model="name" placeholder="Full Name" required />
					<fieldset>
					<div class="input-group-button">
						<button type="submit" class="button">Create</button>
					</div>
				</div>
			</form>
		</div>
	</div>
</div>
</template>

<script>
export default {
	name: 'landing',
	data () {
		return {
			'name': ''
		}
	},
	methods: {
		createInterview () {
			var applicant = this.$resource('applicant/{id}')

			applicant.save({name: this.name}).then(function (response) {
				var interview = this.$resource('interview/{id}')

				interview.save({applicant: response.data.uid}).then(function (response) {
					this.$router.push({name: 'interview', params: { interviewId: response.data.uid }})
				}, function (response) {
					// TODO error handling
				})
			}, function (response) {
				// TODO error handling
			})
		}
	}
}
</script>

<style>
</style>
