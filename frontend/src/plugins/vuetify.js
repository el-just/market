import Vue from 'vue'
import Vuetify, { VApp, VLayout, VTemplate } from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import { Scroll } from 'vuetify/lib/directives'

Vue.use(Vuetify, {
  	iconfont: 'md',
/*
	icons: {
    	'': {
         	component: IconBase,
            props: { // pass props to your component if needed
            	name: 'product'
         	}
		}
    },
*/
  	components: {
    	VApp,
    	VLayout,
  	},
  	directives: {
      	Scroll
  	}
})
