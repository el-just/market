<template>
    <v-card flat>
        <v-img v-if="model.products[0].product.img"
                :aspect-ratio="16/9"
                :src="model.products[0].product.img"
                ></v-img>
        <v-responsive v-else
                :aspect-ratio="16/9"
                >
            <v-container fill-height>
                <v-layout justify-center align-center>
                    <v-icon large>insert_photo</v-icon>
                </v-layout>
            </v-container>
        </v-responsive>
        <v-card-title primary-title>
            <h3 class="title font-weight-regular mb-0">
                {{ model.offer.name[0].toUpperCase()
                        + model.offer.name.slice(1) }}
            </h3>
        </v-card-title>
        <offer-selector
                :class="[
                    'offer-selector',
                    ...[
                        !item.offerModel.offer.weight ?
                            'offer-selector--no-weight' : '',
                        idx === visibleOffers.length - 1 ?
                            'offer-selector--last-row' : '',
                    ]]"

                v-for="(item, idx) in visibleOffers"
                :item="item"
                :offerMenuItems="offerMenuItems()"
                :hideDropdown="idx < visibleOffers.length - 1 ? true : false"

                @offerSelected="selectOffer"
                @actionProceed="processAction"
                ></offer-selector>
        <v-divider></v-divider>
        <v-card-text>
                <div> {{ model.products[0].product.description}} </div>
                <div class="offer-card_country">
                    Страна: {{
                        model.products[0].manufacturer.name[0].toUpperCase()
                        + model.products[0].manufacturer.name.slice(1)}}
                </div>
        </v-card-text>
    </v-card>
</template>

<script>
import Vue from 'vue'
import _ from 'lodash'

import OfferSelector from './offer_selector.vue'

import { mapState, mapGetters, mapMutations, mapActions} from 'vuex'

export default {
    name: 'OfferCard',
    components: {
        OfferSelector,
    },

    props: ['model'],
    data () {
        return {
            showOffersDropdown: false,
            activeOffer: 0,
        }
    },

    created () {
    },
    destroyed () {
    },

    methods: {
        ...mapMutations('cart', [
            'remove'
        ]),

        selectOffer ({changedOffer, item, newOffer}) {
            this.activeOffer = this.model.formats.indexOf(newOffer)
        },

        processAction ({actionName, count, item}) {
            if (actionName === 'remove' && count === 0) {
                this.remove({item})
            }
        },

        offerMenuItems () {
            let selectedItemInCart = false
            let activeCartItem = {
                offerModel: this.model.formats[this.activeOffer],
                parentModel: this.model,
                count: 0,
            }
            let groupActiveOffers = this.cartItems.reduce (
                (result, cartItem) => {
                    if (cartItem.offerModel.offer.parent_id
                            === this.model.offer.id && cartItem.count > 0) {
                        result.push(cartItem.offerModel)
                    }

                    if (activeCartItem.offerModel.offer.id === 
                            cartItem.offerModel.id) {
                        selectedItemInCart = true
                    }

                    return result
                }, [])

            if (!selectedItemInCart) {
                groupActiveOffers.push(
                    this.model.formats[this.activeOffer])
            }

            let ids = _.difference(
                this.model.formats.map((item)=>{return item.offer.id}),
                groupActiveOffers.map((item)=>{return item.offer.id})
            )

            return ids.length ? this.model.formats.filter((item)=>{
                return ids.indexOf(item.offer.id) !== -1
            }) : []
        },
    },

    computed: {
        ...mapState('cart', {
            cartItems: state => state.items,
        }),

        visibleOffers () {
            let selectedItemInCart = false
            let activeCartItem = {
                offerModel: this.model.formats[this.activeOffer],
                parentModel: this.model,
                count: 0,
            }
            let offersInCart = this.cartItems.reduce ((result, item) => {
                if ((item.offerModel.offer.parent_id === this.model.offer.id && 
                        item.count > 0) || activeCartItem.offerModel.offer.id
                            === item.offerModel.offer.id) {
                    result.push (item)
                }

                if (activeCartItem.offerModel.offer.id
                        === item.offerModel.offer.id) {
                    selectedItemInCart = true
                }

                return result
            }, [])

            return !selectedItemInCart?
                    [...offersInCart, activeCartItem]
                    : (offersInCart.length ? offersInCart
                        : [activeCartItem])
        },
    },
    watch: {
    },

}
</script>
<style scoped lang="styl">
.v-card__text
    padding: 12px
    color: #757575

.v-card__title
    padding: 12px

.offer-selector
    padding: 0px 12px
    &.offer-selector--no-weight
        padding-top: 4px
        padding-bottom: 4px

    &.offer-selector--last-row
        margin-bottom: 8px

.offer-card_country
    text-align: right
    margin-top: 6px
</style>
