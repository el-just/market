import Vue from 'vue'
import Vuex from 'vuex'
import VueUid from 'vue-uid';
//import VueNativeSock from 'vue-native-websocket'

import './plugins/vuetify'

import app from './app.vue'
import router from './router.js'
import storeRoot from './store/root.js'


Vue.config.productionTip = false

Vue.use(Vuex)
let store = new Vuex.Store(storeRoot)

Vue.use(VueUid)
/*
Vue.use(VueNativeSock, `ws://${window.location.hostname}:5000/ws`, {
        store,
        format: 'json',
        reconnection: true,
        reconnectionDelay: 3000,
})
*/

new Vue({
  router,
  store,
  render: h => h(app)
}).$mount('#app')
