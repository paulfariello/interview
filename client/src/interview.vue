<template>
<div>
	<template v-if="$loading">
		<loading></loading>
	</template>
	<template v-else>
		<div class="row">
			<div class="small-12 columns">
				<h2><router-link :to="{ name: 'interview', params: { interviewId: interview.uid } }"><i class="fa fa-mortar-board fa-lg fa-fw"></i>{{ interview.applicant.name }}</router-link></h2>
				<router-link class="button" :to="{ name: 'pass', params: { interviewToken: interview.token, index: 0 } }">
					<i class="fa fa-play fa-lg fa-fw"></i>Pass interview
				</router-link>
				<router-link class="button" :to="{ name: 'review', params: { interviewToken: interview.token, index: 1 } }">
					<i class="fa fa-eye fa-lg fa-fw"></i>Review interview
				</router-link>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<progression :progress="interview.exercices.length" :total="interview.exercices.length"></progression>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<h3><i class="fa fa-pencil-square-o fa-lg fa-fw"></i>Exercices</h3>
				<div class="row" v-for="exercice in exercices">
					<div class="columns small-1">
						<div class="switch">
							<input class="switch-input" type="checkbox" v-bind:id="exercice.uid" v-bind:value="exercice.uid" v-model="interview.exercices" v-on:change="selectExercice">
							<label class="switch-paddle" v-bind:for="exercice.uid">
								<span class="show-for-sr" v-html="exercice.question"></span>
							</label>
						</div>
					</div>
					<div class="columns small-5" v-html="exercice.question"></div>
					<div class="columns small-1">
						<span v-for="tag in exercice.tags" class="label">{{tag}}</span>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<form v-on:submit="addExercice">
				<div class="small-12 columns">
					<h3><i class="fa fa-pencil-square-o fa-lg fa-fw"></i>New exercice</h3>
					<h4>Tags</h4>
					<input-tag :klass="tags_input_class" :tags.sync="new_exercice.tags"></input-tag>
				</div>
				<div class="small-12 columns">
					<h4>Question</h4>
					<tinymce v-model="new_exercice.question"></tinymce>
				</div>
				<div class="small-12 columns">
					<button type="submit" class="button fa fa-user-plus">Add</button>
				</div>
			</form>
		</div>
	</template>
</div>
</template>

<script>
import InputTag from 'vue-input-tag'
import TinyMCE from 'components/tinymce'

export default {
	name: 'interview',
	components: {
		'input-tag': InputTag,
		'tinymce': TinyMCE
	},
	data () {
		return {
			'loading': true,
			'interview': {
				'applicant': {'name': ''},
				'exercices': []
			},
			'exercices': [],
			'new_exercice': {'question': '', 'tags': []},
			'tags_input_class': {
				'container': 'tags-input',
				'input': 'input',
				'gap': 'gap',
				'tag': 'label'
			}
		}
	},
	watch: {
		'$route': 'fetchData'
	},
	created () {
		this.fetchData()
	},
	methods: {
		fetchData () {
			this.loading = true
			var exercices = this.$resource('exercice/')

			exercices.get().then(function (response) {
				this.exercices = response.data
			}).catch(function () {
				// TODO handle error
			})

			var interview = this.$resource('interview/{id}')
			interview.get({id: this.$route.params.interviewId}).then(function (response) {
				this.interview = response.data
				var applicant = this.$resource('applicant/{id}')
				applicant.get({id: this.interview.applicant}).then(function (response) {
					this.interview.applicant = response.data
					this.loading = false
				}).catch(function () {
				})
			}).catch(function () {
				// TODO handle error
			})
		},
		selectExercice (e) {
			if (e.target.checked) {
				this.$http.post('interview/' + this.interview.uid + '/exercices/', {
					exercice: e.target.value
				})
			} else {
				this.$http.delete('interview/' + this.interview.uid + '/exercices/' + e.target.value)
			}
		},
		addExercice () {
			var exercice = this.$resource('exercice/')

			exercice.save({
				question: this.new_exercice.question,
				tags: this.new_exercice.tags
			}).then(function (response) {
				this.exercices.push(response.data)
				this.new_exercice.question = ''
				this.new_exercice.tags.length = 0
			}, function (response) {
				// TODO error handling
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
