import 'src/css/main.scss'
import { foundation } from 'foundation-sites/js/foundation.core.js'
$.fn.foundation = foundation
import 'foundation-sites/js/foundation.util.keyboard.js'
import 'foundation-sites/js/foundation.util.box.js'
import 'foundation-sites/js/foundation.util.triggers.js'
import 'foundation-sites/js/foundation.util.mediaQuery.js'
import 'foundation-sites/js/foundation.util.motion.js'
import 'foundation-sites/js/foundation.reveal.js'
import tinymce from 'tinymce'
import 'tinymce/themes/modern/theme'
import 'tinymce/skins/lightgray/content.min.css'
import 'tinymce/skins/lightgray/skin.min.css'
// import 'foundation-datepicker/js/foundation-datepicker.js'
// import 'foundation-datepicker/css/foundation-datepicker.scss'
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import App from './app'
import Landing from './landing'
import Loading from './loading'
import Interview from './interview'
import Pass from './pass'
import Progress from './progress'

Vue.use(VueRouter)
Vue.use(VueResource)

Vue.component('loading', Loading)
Vue.component('progress', Progress)

// Vue.directive('date-picker', {
// 	twoWay: true,
// 	params: ['format', 'language'],
// 	bind: function () {
// 		var self = this
// 		$(this.el).fdatepicker({
// 			initialDate: this.value,
// 			format: this.params.format,
// 			language: this.params.language
// 		}).on('changeDate', function (ev) {
// 			self.set(ev.date)
// 		})
// 	},
// 	update: function (newValue) {
// 		$(this.el).fdatepicker('update', newValue)
// 	}
// })

Vue.directive('tinymce', {
	twoWay: true,
	bind: function () {
		var self = this
		tinymce.init({
			target: this.el,
			skin: false,
			init_instance_callback: function (editor) {
				self.editor = editor
				editor.on('change', function (e) {
					editor.save()
					self.set(self.el.value)
				})
			}
		})
	},
	update: function (value) {
		if (this.editor !== undefined) {
			this.editor.setContent(value)
		}
	}
})

Vue.http.options.root = '/api'

const router = new VueRouter({
	history: false,
	saveScrollPosition: true
})

router.map({
	'/': {
		component: Landing
	},
	'/interview/:interviewId': {
		name: 'interview',
		component: Interview
	},
	'/interview/:interviewToken/pass/:index': {
		name: 'pass',
		component: Pass
	}
})

router.start(App, 'body')
