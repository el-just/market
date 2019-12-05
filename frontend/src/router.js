import Vue from 'vue'
import Router from 'vue-router'

import Market from './views/market.vue'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'market',
      component: Market
    },
    {
      path: '/admin',
      name: 'admin',
      meta: {requireAuth: true},
      component: () => import('./views/admin.vue'),
    },
    {
      path: '/admin/products',
      name: 'products',
      meta: {requireAuth: true},
      component: () => import('./views/products.vue'),
    },
    {
      path: '/admin/offers',
      name: 'offers',
      meta: {requireAuth: true},
      component: () => import('./views/offers.vue'),
    },
    {
      path: '/admin/sales',
      name: 'sales',
      meta: {requireAuth: true},
      component: () => import('./views/sales.vue'),
    },
  ]
})

router.beforeEach((to, from, next) => {
    if (!to.name) {
        next('/')
    }
    if (to.meta.requireAuth) {
        fetch(`/api/user/is_superuser`, {method: 'GET'})
                .then(response => {
                    return response.json()})
                .then(result => {
                    if (result.data.is_superuser) {
                        next()
                    } else {
                        next('/')
                    }
                })
                .catch(exp => {
                    next('/')});
    } else {
        next()
    }
})

export default router
