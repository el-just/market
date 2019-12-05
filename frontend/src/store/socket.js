import Vue from 'vue'

import _ from 'lodash'


export default {
    modules: {
    },
    state: {
        socket: {
            isConnected: false,
            message: null,
            reconnectError: false,
        }
    },
    mutations: {
        SOCKET_ONOPEN (state, event)  {
            Vue.prototype.$socket = event.currentTarget
            state.socket.isConnected = true
        },
        SOCKET_ONCLOSE (state, event)  {
            state.socket.isConnected = false
        },
        SOCKET_ONERROR (state, event)  {
            console.error(state, event)
        },
        // default handler called for all methods
        SOCKET_ONMESSAGE (state, payload)  {
            state.socket.message = payload
        },
        // mutations for reconnect methods
        SOCKET_RECONNECT(state, count) {
            console.info(state, count)
        },
        SOCKET_RECONNECT_ERROR(state) {
            state.socket.reconnectError = true;
        },
    },
    actions: {
    },
    getters: {
    }
}
