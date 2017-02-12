import Vue from 'vue'
import Router from 'vue-router'

import Landing from '../landing'
import Interview from '../interview'
import Pass from '../pass'
import Review from '../review'

Vue.use(Router)

export default new Router({
	history: false,
	saveScrollPosition: true,
	routes: [
		{
			path: '/',
			component: Landing
		},
		{
			path: '/interview/:interviewId',
			name: 'interview',
			component: Interview
		},
		{
			path: '/interview/:interviewToken/pass/:index',
			name: 'pass',
			component: Pass
		},
		{
			path: '/interview/:interviewToken/review/:index',
			name: 'review',
			component: Review
		}
	]
})

