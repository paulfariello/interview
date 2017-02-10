<template>
	<template v-if="$loadingRouteData">
		<loading></loading>
	</template>
	<template v-else>
		<div class="row">
			<div class="small-12 columns">
				<h2><a v-link="{ name: 'interview', params: { interviewId: interview.uid } }"><i class="fa fa-mortar-board fa-lg fa-fw"></i>{{ interview.applicant.name }}</a></h2>
				<a class="button" v-link="{ name: 'pass', params: { interviewToken: interview.token, index: 0 } }">
					<i class="fa fa-play fa-lg fa-fw"></i>Pass interview
				</a>
				<a class="button" v-link="{ name: 'review', params: { interviewToken: interview.token, index: 1 } }">
					<i class="fa fa-eye fa-lg fa-fw"></i>Review interview
				</a>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<progress :progress="interview.exercices | answeredCount" :total="interview.exercices.length"></progress>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<h3><i class="fa fa-pencil-square-o fa-lg fa-fw"></i>Exercices</h3>
				<div class="row" v-for="exercice in exercices">
					<div class="columns small-1">
						<div class="switch">
							<input class="switch-input" type="checkbox" id="{{exercice.uid}}" value="{{exercice.uid}}" v-model="interview.exercices" v-on:change="selectExercice">
							<label class="switch-paddle" for="{{exercice.uid}}">
								<span class="show-for-sr">{{{exercice.question}}}</span>
							</label>
						</div>
					</div>
					<div class="columns small-5">{{{exercice.question}}}</div>
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
					<tags-input :klass="tags_input_class" :tags.sync="new_exercice.tags"></tags-input>
				</div>
				<div class="small-12 columns">
					<h4>Question</h4>
					<textarea v-tinymce="new_exercice.question" required></textarea>
				</div>
				<div class="small-12 columns">
					<button type="submit" class="button fa fa-user-plus">Add</button>
				</div>
			</form>
		</div>
	</template>
</template>

<script>
import TagsInput from 'vue-tagsinput'
export default {
	data () {
		return {
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
	route: {
		data () {
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
				}).catch(function () {
				})
			}).catch(function () {
				// TODO handle error
			})
		}
	},
	methods: {
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
	components: {
		TagsInput
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
