<template>
	<template v-if="$route.params.index > 0">
		<div class="row">
			<div class="small-12 columns">
				<progress :progress="interview.exercices | answeredCount" :total="interview.exercices.length"></progress>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<h2>{{{ exercice.question }}}</h2>
				<span v-for="tag in exercice.tags" class="label float-right">{{tag}}</span>
			</div>
		</div>
		<form>
			<div class="row">
				<div class="small-12 columns">
					<textarea v-tinymce="exercice.answer" :update="save" required></textarea>
				</div>
			</div>
		</form>
		<div class="row">
			<div v-if="exercice.date !== undefined" class="small-12 columns">
				Last save {{ exercice.date }}
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<pagination :total="interview.exercices.length" :current="$route.params.index"></pagination>
			</div>
		</div>
	</template>
	<template v-else>
		<div class="row">
			<div class="small-12 columns">
				<h2><a v-link="{ name: 'pass', params: { interviewToken: interview.token } }"><i class="fa fa-mortar-board fa-lg fa-fw"></i>{{ interview.applicant.name }}</a></h2>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				{{interview.exercices.length}} questions over the following topics:
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<span v-for="tag in tags" class="label">{{tag}}</span>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<a class="button" v-link="{ name: 'pass', params: { interviewToken: interview.token, index: 1 } }">Let's go !</a>
			</div>
		</div>
	</template>
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
			'exercice': {
				'uid': '',
				'question': '',
				'index': 0,
				'answer': '',
				'date': '',
				'tags': []
			}
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

			if (this.$route.params.index > 0) {
				var exercice = this.$resource('interview/{token}/exercices/{index}')
				exercice.get({
					token: this.$route.params.interviewToken,
					index: this.$route.params.index
				}).then(function (response) {
					this.exercice = response.data
					var answer = this.exercice.history[this.exercice.history.length - 1]
					this.exercice.answer = answer.answer
					this.exercice.date = answer.date
				}).catch(function () {
				})
			}
		}
	},
	methods: {
		save () {
			var exercice = this.$resource('interview/' + this.$route.params.interviewToken + '/exercices/' + this.exercice.uid)

			exercice.update({answer: this.exercice.answer}).then(function (response) {
				this.exercice.date = response.data.date
			}, function (response) {
			})
		}
	},
	filters: {
		answeredCount (exercices) {
			var count = 0
			// for (var i in exercices) {
			// 	count += exercices[i].answer.length > 0
			// }
			return count
		}
	}
}
</script>
