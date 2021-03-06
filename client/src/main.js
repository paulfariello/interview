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
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import App from './app'
import Landing from './landing'
import Loading from './loading'
import Interview from './interview'
import Pass from './pass'
import Review from './review'
import Progress from './progress'
import Pagination from './pagination'

Vue.use(VueRouter)
Vue.use(VueResource)

Vue.component('loading', Loading)
Vue.component('progress', Progress)
Vue.component('pagination', Pagination)

Vue.directive('tinymce', {
	params: ['update'],
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
					if (self.params.update) {
						self.params.update(self.el.value)
					}
				})
			}
		})
	},
	update: function (value) {
		if (this.editor !== undefined) {
			if (value !== null) {
				this.editor.setContent(value)
			} else {
				this.editor.setContent('')
			}
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
	},
	'/interview/:interviewToken/review/:index': {
		name: 'review',
		component: Review
	}
})

router.start(App, 'body')
