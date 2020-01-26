import _ from 'lodash'
import Vue from 'vue'

let debounceInterval = 300
export default {
    namespaced: true,
    modules: {
    },
    state: {
        activeTab: 1,
        categories: [
            'Всё',
            'Фрукты и Ягоды',
            'Овощи',
            'Зелень',
            'Сезонное',
        ],
        items: [],
        fullItems: [],
        carousel: [
            'https://storage.yandexcloud.net/veggies/market.jpg',
            'https://storage.yandexcloud.net/veggies/mango.jpg',
            'https://storage.yandexcloud.net/veggies/persimmon.jpg',
        ],

        rowsPerPageItems: [12],

        offerModel: undefined,
        offerDialogShowed: false,
    },
    mutations: {
        update: (state, items) => {
            state.fullItems = items
            state.items = state.fullItems.slice (0, 11)
        },

        updateTab: (state, tabId) => {
            state.activeTab = tabId
        },

        nextItems: state => {
            state.items = state.fullItems.slice(0, state.items.length + 12)
        },

        toggleDialog: (state, offerId) => {
            state.offerDialogShowed = offerId ? true : false;
        },

        setOfferModel: (state, model) => {
            state.offerModel = model
        },

        setOfferDialogShowed: (state, value) => {
            state.offerDialogShowed = value
        }
    },
    actions: {
        setActiveTab: ({commit, dispatch}, tabId) => {
            commit('updateTab', tabId)
            dispatch('load')
        },

        setActiveOffer: ({commit, dispatch}, offerId) => {
            commit('toggleDialog', offerId)
            fetch('/api/market/list', {
                method: 'POST',
                body: JSON.stringify({
                    offer_id: offerId,
                }),
            })
            .then(response => {
                return response.json()})
            .then(result => {
                commit('setOfferModel', result[0])})
            .catch(exp => {
                console.error(exp)});
        },

        load: _.debounce (({commit, state, rootState}) => {
            fetch('/api/market/list', {
                method: 'POST',
                body: JSON.stringify({
                    category: state.activeTab,
                    search_text: rootState.searchText || null,
                }),
            })
            .then(response => {
                return response.json()})
            .then(result => {
                commit('update', result)})
            .catch(exp => {
                console.error(exp)});
        }, debounceInterval)
    },
    getters: {
        total: state => {
            return state.items.length
        },

        hasMore: state => {
            return (state.fullItems.slice(0, state.items.length + 12).length
                        > state.items.length)
        }
    }
}
