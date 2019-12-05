<template>
<v-layout class="basic-layout">
    <div v-if="items.length"
            class="main-container"
            >
        <v-layout wrap
                v-for="(item, idx) in items"
                :key="item.offerModel.offer.id"
                class="cart-item"
                >
            <v-flex xs8 sm8 md8 lg8 xl8 
                    @click="toggleItem({item, idx})"
                    class="cart-item-head__name font-weight-medium"
                    >
                {{ item.count }}
                {{ item.offerModel.entity.declensions ?
                    new countForms(item.offerModel.entity.declensions)
                    .setCount(item.count) : item.offerModel.entity.name
                }} 
            </v-flex>
            <v-flex xs4 sm4 md4 lg4 xl4
                    class="cart-item-head__amount"
                    >
                {{ multiply(item.count, item.offerModel.offer.price) }}₽
            </v-flex>
            <v-flex xs12 sm12 md12 lg12 xl12
                    v-if="nodeVisible(item)"
                    class="cart-item__editor"
                    >
                <v-layout wrap
                        v-for="(offerItem, offerIdx) in visibleOffers(item)"
                        >
                    <v-flex xs12 sm12 md12 lg12 xl12 style="padding-right: 12px">
                        <div class="cart-item__padding-container
                                font-weight-medium">
                            {{ item.count }}&nbsp;
                        </div>
                        <offer-selector small
                            :item="offerItem"
                            :meta="{parent: item}"

                            :offerMenuItems="offerMenuItems(offerItem)"
                            :hideDropdown="
                                offerIdx === visibleOffers(item).length - 1 ?
                                false : true"
                            @offerSelected="selectOffer"
                            @actionProceed="processAction"
                            ></offer-selector>
                    </v-flex>
                </v-layout>
            </v-flex>
        </v-layout>
        <v-layout class="cart-summary font-weight-regular">
            <v-flex>
                {{ items.length }} {{
                    new countForms(['позиция', 'позиции', 'позиций']).setCount(
                            items.length)}},
                <span
                        class="font-weight-regular body-2 cart-summary__weight">
                    &#8776{{ weight }} кг
                </span>
                </br>
                К оплате
            </v-flex>
            <v-flex align-self-end
                    class="cart-summary__amount">
                {{ amount }}₽
            </v-flex>
        </v-layout>
    </div>
    <v-layout justify-center align-center
            v-else
            :class="['empty-container', validationErrorClass]"
            >
        <h3 class="subheading">
            Корзина пуста
        </h3>
    </v-layout>
</v-layout>
</template>
<script>
import Big from 'big.js'

import utils from '../utils.js'
import OfferSelector from './offer_selector.vue'

import { mapGetters, mapState, mapMutations, mapActions } from 'vuex'


export default {
    name: 'CartView',
    components: {
        OfferSelector
    },

    props: [],
    data () {
        return {
            validationErrorClass: '',

            countForms: utils.CountForms,
        }
    },

    created () {
    },
    destroyed () {
    },

    methods: {
        ...mapMutations ('cart', [
            'clearCartItems',
        ]),

        validate () {
            let count = this.items.reduce((r, v)=>{
                return v.count + r
            }, 0)
            this.validationErrorClass = count > 0 ? '' : 'validation-error'

            if (count === 0 && this.items.length) {
                this.clearCartItems()
            }

            return count > 0
        },

        processAction ({actionName, count, item, meta}) {
            if (actionName === 'remove' && count === 0
                    && item.offerModel.offer.id !== meta.parent.offerModel.offer.id) {
                this.removeSelected ({item, meta})
            }
        },

        nodeVisible (item) {
            return this.nodesOpened.findIndex(openedItem => {
                    return openedItem.offerModel.offer.id
                        === item.offerModel.offer.id
                    }) !== -1
        },

        multiply (count, amount) {
            return Big(amount).times(count)
        },

        ...mapActions('cart/view', [
            'selectOffer',
            'removeSelected',
            'toggleItem',
        ]),
    },

    computed: {
        ...mapState('cart', [
            'items',
        ]),
        ...mapGetters('cart', [
            'count',
            'weight',
            'amount',
        ]),

        ...mapState('cart/view', [
            'selected',
            'opened',
            'nodesOpened',
        ]),
        ...mapGetters('cart/view', [
            'visibleOffers',
            'offerMenuItems',
        ]),
    },
    watch: {
    },
}
</script>
<style scoped lang="styl">
border_color = #f2f0b3
background_color = #ffffe0
basic_font_color = #344816
item_name_text = #a09c08
item_name_text_hover = #d8d10e
divider_color = #bdbdbd
error_color_focused = #ffa559

.main-container
    width: 100%

    padding-top: 12px
    border-radius: 2px
    color: basic_font_color
    background-color: background_color
    border: 1px solid border_color

    .cart-item
        margin-bottom: 8px
        padding: 0 12px

        .cart-item-head__name
            cursor: pointer
            user-select: none

            transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1)
            color: item_name_text

            &:hover
                color: item_name_text_hover
        .cart-item-head__amount
            text-align: right

        .cart-item__divider-container
            padding: 4px 64px 4px 28px
        .cart-item__divider
            border-color: divider_color

        .cart-item__padding-container
            float: left
            color: background_color

.empty-container
    min-height: 120px
    color: #9e9e9e

    &.validation-error
        color: error_color_focused

.cart-summary
    border-top: 1px solid #efe823
    font-size: 18px

    padding: 12px

    .cart-summary__amount
        text-align: right

    .cart-summary__weight
        color: #9e9e9e
        font-size: 12px !important
        
</style>
