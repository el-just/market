import Vue from 'vue'
import Big from 'big.js'

import _ from 'lodash'

import cartView from './cart_view.js'

export default {
    namespaced: true,
    modules: {
        view: cartView,
    },
    state: {
        personName: undefined,
        personPhone: undefined,
        personAddress: undefined,
        personEmail: undefined,
        deliveryDate: undefined,
        deliveryInterval: 'с 12:00 до 15:00',
        paymentType: 'Наличными',
        changeFrom: undefined,
        extraFlags: [true, false],
        specialInstructions: undefined,
        acceptPolicy: undefined,

        deliveryIntervalItems: [
            'с 12:00 до 15:00',
            'с 15:00 до 18:00',
            'с 18:00 до 21:00',
            ],
        paymentTypeItems: [
            'Наличными',
            'Переводом на Сбербанк курьеру',
        ],

        items: [],
    },
    mutations: {
        add: (state, item) => {
            state.items.push (item)

            fetch(`/api/order/save_cart_state`, {
                    method: 'POST',
                    credentials: 'include',
                    body: JSON.stringify({cart:state}),
            })
        },

        remove: (state, {idx, item}) => {
            state.items = _.remove(state.items, model => {
                    return model.offerModel.offer.id !== item.offerModel.offer.id})

            fetch(`/api/order/save_cart_state`, {
                    method: 'POST',
                    credentials: 'include',
                    body: JSON.stringify({cart:state}),
            })
        },

        update: (state, {offerModel, count}) => {
            let idx = state.items.findIndex (item => {
                return offerModel.offer.id === item.offerModel.offer.id
            })
            Vue.set (state.items[idx], 'count', count)

            fetch(`/api/order/save_cart_state`, {
                    method: 'POST',
                    credentials: 'include',
                    body: JSON.stringify({cart:state}),
            })
        },

        replace: (state, items) => {
            state.items = items
        },

        setOrderDetails: (state, {item, value}) => {
            state[item] = value
        },

        clearCartItems: state => {
            state.items = []
            fetch(`/api/order/save_cart_state`, {
                    method: 'POST',
                    credentials: 'include',
                    body: JSON.stringify({cart:state}),
            })
        },

        updatePersonName: (state, value) => {
            state.personName = value
        },
        updatePersonPhone: (state, value) => {
            state.personPhone = value
        },
        updatePersonAddress: (state, value) => {
            state.personAddress = value
        },
        updatePersonEmail: (state, value) => {
            state.personEmail = value
        },
        updateDeliveryDate: (state, value) => {
            state.deliveryDate = value
        },
        updateDeliveryInterval: (state, value) => {
            state.deliveryInterval = value
        },
        updatePaymentType: (state, value) => {
            state.paymentType = value
        },
        updateChangeFrom: (state, value) => {
            state.changeFrom = value
        },
        updateExtraFlags: (state, value) => {
            state.extraFlags = value
        },
        updateSpecialInstructions: (state, value) => {
            state.specialInstructions = value
        },
        updateAcceptPolicy: (state, value) => {
            state.acceptPolicy = value
        },
    },
    actions: {
        updateCount: ({commit, state}, model) => {
            model.count = model.count < 0 ? 0 : model.count

            let idx = state.items.findIndex (item => {
                return (model.offerModel.offer.id
                        === item.offerModel.offer.id)
            })

            if (idx !== -1) {
                commit ('update', model)
            } else if (model.count > 0) {
                commit ('add', model)
            }

            ym(56243326, 'reachGoal', 'updateCart');
        },

        remove: ({commit, state}, {idx, item}) => {
            commit('remove', {idx, item})
        }
    },
    getters: {
        count: state => {
            return state.items.reduce ((result, item)=>{
                result = Big(item.count).plus(result)
                return result
            }, 0)
        },

        weight: state => {
            return state.items.reduce ((result, item)=>{
                result = Big(item.offerModel.offer.weight || 1)
                         .times(item.count).plus(result)

                return result
            }, 0)
        },

        amount: state => {
            return state.items.reduce ((result, item)=>{
                result = Big(item.offerModel.offer.price)
                         .times(item.count).plus(result)

                return result
            }, 0)
        },

        total: (state, getters) => {
            return Big(getters.amount).plus(getters.choice)
                    .plus(getters.deliveryPrice)
        },

        choice: (state, getters) => {
            return getters.amount <= 2000 ? 200
                    : Big((getters.amount / 1000) | 0).times(100)
        },

        deliveryPrice: state => {
            return 400
        },
    }
}
