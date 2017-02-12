<template>
<div>
	<template v-if="$loading">
		<loading></loading>
	</template>
	<template v-else>
		<div class="row">
			<div class="small-12 columns">
				<progression :progress="interview.exercices.length" :total="interview.exercices.length"></progression>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<h2 v-html="exercice.question"></h2>
				<span v-for="tag in exercice.tags" class="label float-right">{{tag}}</span>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<div class="callout" v-if="exercice.history.length > 0" v-html="exercice.history[current].answer"></div>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns" v-if="exercice.history.length > 0">
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
				<button v-if="playing" class="fa fa-pause float-left" v-on:click="pause"><span class="show-for-sr">Pause</span></button>
				<button v-else class="fa fa-play float-left" v-on:click="play"><span class="show-for-sr">Play</span></button>
				<div class="progress" role="progressbar" tabindex="0" v-bind:aria-valuenow="position() * 100" aria-valuemin="0" v-bind:aria-valuetext="position() * 100 + ' percent'" aria-valuemax="100">
					<div class="progress-meter" v-bind:style="{width: position() * 100 + '%'}"></div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="small-12 columns">
					<pagination :total="interview.exercices.length" :current="$route.params.index"></pagination>
			</div>
		</div>
	</template>
</div>
</template>

<script>
export default {
	name: 'review',
	data () {
		return {
			'loading': true,
			'interview': {
				'applicant': {'name': ''},
				'token': '',
				'exercices': []
			},
			'exercice': {
				'uid': '',
				'question': '',
				'answers': {},
				'index': 0,
				'history': [],
				'tags': []
			},
			'current': 0,
			'playing': false
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
					this.current = this.exercice.history.length - 1
				}).catch(function () {
				})
			}
		},
		play () {
			this.playing = true
			if (this.current + 1 >= this.exercice.history.length) this.current = 0
			this.render()
		},
		pause () {
			this.playing = false
		},
		render () {
			if (!this.playing) return
			this.current++
			if (this.current + 1 >= this.exercice.history.length) return
			var timeout = Date.parse(this.exercice.history[this.current + 1].date) - Date.parse(this.exercice.history[this.current].date)
			setTimeout(this.render, timeout)
		},
		position () {
			if (this.exercice.history.length > 0) {
				var begin = Date.parse(this.exercice.history[0].date)
				var current = Date.parse(this.exercice.history[this.current].date)
				var end = Date.parse(this.exercice.history[this.exercice.history.length - 1].date)
				return (current - begin) / (end - begin)
			} else {
				return 1
			}
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
