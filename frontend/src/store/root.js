import Vue from 'vue'

import cart from './cart.js'
import market from './market.js'
import socket from './socket.js'
import user from './user.js'

export default {
    modules: {
        cart: cart,
        market: market,
        user: user,
        socket: socket,
    },
    state: {
        searchText: null,
        scroll: {
            offset: null,
            clientHeight: null,
            fullHeight: null,
        },
        showMore: false,
        showNavigation: undefined,
        stage: undefined,
    },
    mutations: {
        updateSearchText: (state, text) => {
            state.searchText = text
        },

        setScroll: (state, scroll) => {
            state.scroll = scroll
        },

        setShowMore: (state, value) => {
            state.showMore = value
        },

        setShowNavigation: (state, value) => {
            state.showNavigation = value
        },

        setStage: (state, value) => {
            state.stage = value
        },
    },
    actions: {
        setSearchText: ({commit}, text) => {
            commit('updateSearchText', text)
        }
    },
    getters: {
    }
}
