<template>
<v-card style="width: 100%">
    <v-toolbar card flat style="position: fixed; width: 900px; z-index: 2">
        <v-toolbar-title>
            <v-text-field solo flat
                    class="name"
                    v-model="offerModel.offer.name"
                    label="Offer name"
                    >
            </v-text-field>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
            <v-btn flat
                    @click="save">
                save
            </v-btn>
            <v-btn flat
                    @click="toggleOffer">
                {{ offerModel.entity.paused ? 'unpause' : 'pause' }}
            </v-btn>
            <v-btn flat
                    @click="deleteOffer">
                delete
            </v-btn>
        </v-toolbar-items>
    </v-toolbar>
    <v-layout row style="padding-top:64px">
        <v-flex xs6 sm6 md6 lg6 xl6 style="padding: 54px 12px 0 36px">
            <v-text-field
                label="Declensions 1"
                v-model="offerModel.entity.declensions[0]"
                >
            </v-text-field>
            <v-text-field
                label="Declensions 2,3,4"
                v-model="offerModel.entity.declensions[1]"
                >
            </v-text-field>
            <v-text-field
                label="Declensions 0,5,6,7,8,9,1x"
                v-model="offerModel.entity.declensions[2]"
                >
            </v-text-field>
        </v-flex>
        <v-flex xs6 sm6 md6 lg6 xl6 text-xs-center>
            <h1 class="headline">Products</h1>
            <v-list>
                <v-list-tile
                        v-for="productModel in offerModel.products"
                        :key="productModel.entity.id"
                        >
                    <v-flex class="font-weight-medium">
                        {{ productModel.entity.name }}
                        ({{ productModel.manufacturer.name }})
                        <v-btn flat icon
                                @click="removeProduct(productModel)">
                            <v-icon>clear</v-icon>
                        </v-btn>
                    </v-flex>
                </v-list-tile>
            </v-list>
            <v-btn flat v-if="!productSelector"
                    @click="productSelector = true">
                + Add
            </v-btn>
            <v-autocomplete v-else
                    v-model="selectedProduct"
                    :items="products"
                    :selectedItems="productSelection"
                    persistent-hint
                    item-text="entity.name"
                    item-value="entity.id"
                    ref="productSelector"
                    >
            </v-autocomplete>
        </v-flex>
    </v-layout>
    <v-layout row>
        <v-flex text-xs-center style="padding-top: 24px">
            <h1 class="headline">Formats</h1>
        </v-flex>
    </v-layout>
    <v-layout row wrap>
        <v-flex xs6 sm6 md6 lg6 xl6>
            <v-list>
                <v-list-tile
                        v-for="format in offerModel.formats"
                        :key="format.id"
                        @click="formatModel = format"
                        >
                    <v-layout row>
                        <div>
                            <v-btn flat icon
                                    @click="removeOffer(item)">
                                <v-icon>clear</v-icon>
                            </v-btn>
                            <span>
                                {{ format.offer.name }} | 
                            </span>
                            <span>
                                 | {{ format.offer.weight }} | 
                            </span>
                            <span>
                                | {{ format.offer.price }} | 
                            </span>
                            <span>
                                | {{ format.offer.count_type === 1 ? 'float'
                                : 'integer' }}
                            </span>
                        </div>
                    </v-layout>
                </v-list-tile>
            </v-list>
            <v-flex text-xs-center>
                <v-btn flat
                        @click="addOffer">
                    + Add
                </v-btn>
            </v-flex>
        </v-flex>
        <v-flex xs6 sm6 md6 lg6 xl6 style="padding: 12px 36px 12px 12px">
            <v-text-field
                    label="Name"
                    v-model="formatModel.offer.name"
                    >
            </v-text-field>
            <v-text-field
                    label="Entity name"
                    v-model="formatModel.entity.name"
                    >
            </v-text-field>
            <v-text-field
                    label="Declensions 1"
                    v-model="formatModel.entity.declensions[0]"
                    >
            </v-text-field>
            <v-text-field
                    label="Declensions 2,3,4"
                    v-model="formatModel.entity.declensions[1]"
                    >
            </v-text-field>
            <v-text-field
                    label="Declensions 0,5,6,7,8,9,1x"
                    v-model="formatModel.entity.declensions[2]"
                    >
            </v-text-field>
            <v-text-field
                    label="Offer weight"
                    v-model="formatModel.offer.weight"
                    type="number"
                    >
            </v-text-field>
            <v-text-field
                    label="Offer price"
                    v-model="formatModel.offer.price"
                    type="number"
                    >
            </v-text-field>
            <v-select
                    :items="[0, 1]"
                    label="Offer count type"
                    persistent-hint

                    v-model="formatModel.offer.count_type"
                    ></v-select>
            <v-text-field
                    label="Priority"
                    v-model="formatModel.offer.priority"
                    type="number"
                    >
            </v-text-field>
            <v-text-field
                    label="Sellers price"
                    v-model="formatModel.offer.sellers_price"
                    type="number"
                    >
            </v-text-field>
        </v-flex>
    </v-layout>
</v-card>
</template>
<script>
import Vue from 'vue'
import { Offer, Format } from '../db/offer.js'

export default {
    name: 'OfferDialog',
    components: {
    },

    props: ['model', 'products'],
    data () {
        return {
            offerModel: Offer(),
            formatModel: Format(),

            productSelector: false,
            selectedProduct: null,
            productSelection: [],
        }
    },

    created () {
    },

    methods: {
        save () {
            fetch(`/api/offer/update_or_create`, {
                    method: 'POST',
                body: JSON.stringify({models:[this.offerModel]})
                })
                .then(response => {
                    return response.json()})
                .then(result => {
                    })
                .catch(exp => {
                    console.log(exp)});
        },

        deleteOffer () {
            fetch(`/api/offer/delete`, {
                    method: 'POST',
                body: JSON.stringify({models:[this.offerModel]})
                })
                .then(response => {
                    return response.json()})
                .then(result => {
                    })
                .catch(exp => {
                    console.log(exp)});
        },

        addOffer () {
            let formatModel = Format(this.offerModel.offer.id) 
            this.offerModel.formats.push(formatModel)
            this.formatModel = formatModel
        },

        toggleOffer () {
            Vue.set (this.offerModel.entity, 'paused',
                     !this.offerModel.entity.paused)
        },

        removeFormat(formatModel) {
            this.offerModel.formats = this.offerModel.formats.filter(model=>{
                return model !== formatModel
            })

            if (this.formatModel === formatModel) {
                this.formatModel = this.offerModel.formats[0]
                                   ? this.offerModel.formats[0]
                                   : Format(this.offerModel.offer["id"])
            }
        },

        removeProduct (productModel) {
            this.offerModel.products = this.offerModel.products.filter(model=>{
                return model !== productModel
            })
        }
    },

    computed: {
    },
    watch: {
        model () {
            if (this.model) {
                this.offerModel = this.model
                this.formatModel = this.offerModel.formats[0]
                                   ? this.offerModel.formats[0]
                                   : Format(this.offerModel.offer.id)
            } else {
                this.offerModel = Offer()
                this.formatModel = Format(this.offerModel.offer.id)
            }
        },

        selectedProduct () {
            if (this.selectedProduct) {
                this.offerModel.products.push(this.products.find(product => {
                    return product.entity.id === this.selectedProduct
                }))

                this.selectedProduct = null
                this.productSelector = false
            }
        },
    },
}
</script>
<style scoped lang="styl">
.headline
    margin: 12px
.name >>> .v-input__slot
    background-color: #f5f5f5 !important
</style>
