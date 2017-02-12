import 'src/css/main.scss'
import { foundation } from 'foundation-sites/js/foundation.core.js'
$.fn.foundation = foundation
import 'foundation-sites/js/foundation.util.keyboard.js'
import 'foundation-sites/js/foundation.util.box.js'
import 'foundation-sites/js/foundation.util.triggers.js'
import 'foundation-sites/js/foundation.util.mediaQuery.js'
import 'foundation-sites/js/foundation.util.motion.js'
import 'foundation-sites/js/foundation.reveal.js'
import Vue from 'vue'
import VueResource from 'vue-resource'

import App from './app'
import Loading from './components/loading'
import Progress from './components/progress'
import Pagination from './components/pagination'
import router from './router'

Vue.use(VueResource)

Vue.component('loading', Loading)
Vue.component('progression', Progress)
Vue.component('pagination', Pagination)

Vue.http.options.root = '/api'

/* eslint-disable no-new */
new Vue({
	name: 'main',
	el: '#app',
	router: router,
	template: '<app/>',
	components: { App }
})
