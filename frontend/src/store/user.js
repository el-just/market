import Vue from 'vue'

import _ from 'lodash'


let debounceInterval = 300
export default {
    namespaced: true,
    modules: {
    },
    state: {
        auth: false,
    },
    mutations: {
        setAll: (state, data) => {
            Object.assign(state, data)
        },

        setAuth: (state, value) => {
            state.auth = value
        },
    },
    actions: {
    },
    getters: {
    }
}
