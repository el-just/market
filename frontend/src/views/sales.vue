<template>
    <v-container>
		<v-flex ml-4 class="title">
    		<router-link to="/admin">cd ..</router-link>
		</v-flex>
        <v-menu lazy offset-y
                v-model="datePickerMenu"
                :close-on-content-click="false"
                :nudge-right="12"

                transition="scale-transition"
                attach=".delivery-date-picker"
                >
            <template v-slot:activator="{}">
                <v-icon
                        @click="datePickerMenu = true">
                    event
                </v-icon>
                <span
                        class="delivery-date-picker
                               font-weight-medium">
                    <span>{{ deliveryDateFormatted }}</span>
                </span>
            </template>
            <v-date-picker no-title
                    color="#eae300"
                    v-model="deliveryDate"
                    @input="datePickerMenu = false"
                    locale="ru-ru"
                    >
            </v-date-picker>
        </v-menu>
        <v-btn
                @click="sendEmail"
                >
            email
        </v-btn>
        <v-tabs
                v-model="activeTab"
                color="white"
                slider-color="yellow"
                >
            <v-tab
                    ripple
                    >
                Orders
            </v-tab>
            <v-tab
                    ripple
                    >
                Summary
            </v-tab>
            <v-tab-item>
                <v-data-iterator
                        :items="orders"
                        content-tag="v-layout"
                        row
                        wrap
                        >
                    <template v-slot:item="{ item }">
                        <v-card class="order-container" flat>
                            <v-layout>
                                <v-flex xs6 sm6 md6 lg6 xl6>
                                    Order {{ item.order.id }}
                                    <div v-for="offer in item.offers">
                                        {{ offer.count}}
                                        {{ new countForms(
                                            offer.entity.declensions)
                                                .setCount(item.count)
                                        }}
                                    </div>
                                    <div>
                                        Total price: {{ item.order.amount}}
                                    </div>
                                    <div>
                                        Change from: {{ item.order.change_from}}
                                    </div>
                                </v-flex>
                                <v-flex xs6 sm6 md6 lg6 xl6>
                                    <div>
                                        Name: {{ item.order.person_name}}
                                    </div>
                                    <div>
                                        Phone: {{ item.order.person_phone}}
                                    </div>
                                    <div>
                                        Address: {{ item.order.person_address}}
                                    </div>
                                    <div>
                                        Instructions: {{ 
                                            item.order.special_instructions}}
                                    </div>
                                    <div>
                                        Delivery date: {{
                                            item.order.delivery_date}}
                                    </div>
                                    <div>
                                        Delivery interval: {{ 
                                            deliveryIntervalItems[
                                                item.order.delivery_interval]}}
                                    </div>
                                    <div>
                                        Payment type: {{ 
                                            paymentTypeItems[
                                                item.order.payment_type]}}
                                    </div>
                                </v-flex>
                            </v-layout>
                        </v-card>
                    </template>
                </v-data-iterator>
            </v-tab-item>
            <v-tab-item>
                Total orders: {{totalOrders}}
                Total positions: {{totalPositions}}
                Total money: {{totalMoney}}
                <v-data-table
                        :headers="offersHeaders"
                        :items="offers"
                        class="elevation-1"
                        hide-actions
                        >
                    <template v-slot:items="props">
                        <td>
                            {{ props.item.entity.declensions[0] }}
                        </td>
                        <td class="text-xs-right">
                            {{ props.item.weight }}</td>
                        <td class="text-xs-right">
                            {{ props.item.count }}</td>
                        <td class="text-xs-right">
                            {{ props.item.price }}</td>
                    </template>
                </v-data-table>
            </v-tab-item>
        </v-tabs>
    </v-container>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex'
import Big from 'big.js'
import utils from '../utils.js'

export default {
    name: 'Sales',
    components: {
    },

    data () {
        return {
            orders: [],
            offers: [],
            activeTab: 0,
            datePickerMenu: false,
            deliveryDate: undefined,

            offersHeaders: [
                { text: 'Name', value: 'parent_name' },
                { text: 'Weight', value: 'total_weight' },
                { text: 'Count', value: 'total_count' },
                { text: 'Total price', value: 'total_price' },
            ],
            countForms: utils.CountForms,
        }
    },

    created () {
        this.deliveryDate = this.defaultDate
        this.loadOrders()
    },

    methods: {
        loadOrders () {
            fetch(`/api/order/list`, {
                method: 'POST',
                body: JSON.stringify({
                    "delivery_date":this.deliveryDate,
                }),
            })
            .then(response => {
                return response.json()
            })
            .then(result => {
                this.orders = result
            })
            .catch(exp => {
                console.log(exp)});
        },
        loadSummary () {
            fetch(`/api/order/summary`, {
                method: 'POST',
                body: JSON.stringify({
                    "delivery_date":this.deliveryDate,
                }),
            })
            .then(response => {
                return response.json()
            })
            .then(result => {
                this.offers = result
            })
            .catch(exp => {
                console.log(exp)});
            
        },

        sendEmail () {
            fetch(`/api/order/email_delivery_summary`, {
                method: 'POST',
                body: JSON.stringify({delivery_date: this.deliveryDate})
            })
        },
    },

    computed: {
        ...mapState('cart', [
            'deliveryIntervalItems',
            'paymentTypeItems',
        ]),

        deliveryDateFormatted () {
            if (this.deliveryDate) {
                let splittedDate = this.deliveryDate.split('-')

                return [splittedDate[2], splittedDate[1],
                    splittedDate[0].substr(-2)].join('.')
            } else {
                return ''
            }
        },

        defaultDate () {
            let today = new Date ()
            let result = new Date (today)

            result.setDate (result.getDate() + 1)
            return result.toISOString().split('T')[0]
        },

        totalOrders () {
            return this.orders.length
        },
        totalMoney () {
            return this.offers.reduce ((result, model)=>{
                return Big(model.price).plus(result)
            }, 0)
        },
        totalPositions () {
            return this.offers.length
        },
    },

    watch: {
        activeTab () {
            if (this.activeTab === 1) {
                this.loadSummary()
            }
        }
    },
}
</script>
<style scoped lang="styl">
.order-container
    border: 1px black solid
    width: 100%
</style>
