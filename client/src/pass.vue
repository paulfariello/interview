<template>
	<div class="row" v-if="$route.params.index < 1">
		<div class="small-12 columns">
			<h2><a v-link="{ name: 'pass', params: { interviewToken: interview.token } }"><i class="fa fa-mortar-board fa-lg fa-fw"></i>{{ interview.applicant.name }}</a></h2>
		</div>
		<div class="small-12 columns">
			{{interview.exercices.length}} questions over the following topics:
		</div>
		<div class="small-12 columns">
			<span v-for="tag in tags" class="label">{{tag}}</span>
		</div>
		<div class="small-12 columns">
			<a class="button" v-link="{ name: 'pass', params: { interviewToken: interview.token, index: 1 } }">Let's go !</a>
		</div>
	</div>
</template>

<script>
export default {
	data () {
		return {
			'interview': {
				'applicant': {'name': ''},
				'token': '',
				'exercices': []
			},
			'tags': {},
			'answer': ''
		}
	},
	route: {
		data () {
			var interview = this.$resource('interview/{token}/pass')
			interview.get({token: this.$route.params.interviewToken}).then(function (response) {
				this.interview = response.data
				var applicant = this.$resource('applicant/{id}')
				applicant.get({id: this.interview.applicant}).then(function (response) {
					this.interview.applicant = response.data
				}).catch(function () {
				})
				for (var i in this.interview.exercices) {
					var tag = this.interview.exercices[i]
					if (tag in this.tags) {
						this.tags[tag]++
					} else {
						this.tags[tag] = 1
					}
				}
			}).catch(function () {
				// TODO handle error
			})
		}
	}
}
</script>
