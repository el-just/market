<template>
<v-container style="height:100%; padding: 0;">
    <v-container fluid fill-height style="padding: 0"
            transition="slide-x-reverse-transition"
            v-if="orderDialogShowed"
            >
        <v-layout column justify-center v-if="orderCreating">
            <v-flex 
                    xs4 sm4 md4 lg4 xl4
                    text-xs-center
                    >
                <v-progress-circular
                        :size="67"
                        color="#a2e043"
                        indeterminate
                ></v-progress-circular>
                <div
                        class="order-dialog_order-creating-text"
                        >
                    Создаём заказ ...
                </div>
            </v-flex>
        </v-layout>
        <v-layout column v-else
                style="color: rgba(0, 0, 0, 0.72)">
            <v-flex style="font-size: 16px; padding: 12px 16px 0 16px"
                    xs3 sm3 md3 lg3 xl3
                    text-xs-right
                    >
                <v-btn flat icon
                        color="#ffa559"
                        style="margin: 0; float: right"
                        @click="closeOrder"
                        >
                    <v-icon large>close</v-icon>
                </v-btn>
            </v-flex>
            <v-flex style="font-size: 16px; padding: 0 16px" class=""
                    xs1 sm1 md1 lg1 xl1
                >
                <div
                        style="text-align: center"
                        class="headline"
                        >
                    <span>Заказ №{{createdOrder.id}}</span>
                    <span style="font-size: 18px; color: #9e9e9e">
                        ({{createdOrder.amount}}₽,
                    </span>
                    <span style="font-size: 14px; color: #9e9e9e">
                        &#8776{{createdOrder.weight}} кг<!--
                 --></span><!--
                 --><span style="font-size: 18px; color: #9e9e9e">)</span>
                </div>
            </v-flex>
            <v-flex style="font-size: 16px; padding: 0 16px" class=""
                    xs1 sm1 md1 lg1 xl1
                >
                <div style="margin-top: 12px;">
                    <span>Доставим </span>
                    <span class="font-weight-bold">
                        {{orderView.date}}
                    </span>
                    <span> с </span>
                    <span class="font-weight-bold"> 
                        {{orderView.from}} </span>
                    <span class="font-weight-medium"> до </span>
                    <span class="font-weight-bold">
                        {{orderView.till}}
                    </span>
                </div>
                <div>
                    <span>Оплата</span>
                    <span class="font-weight-bold">
                        {{orderView.paymentType}}<!--
                 --></span><!--
                 --><span><!--
                     -->{{orderView.changeFrom}}
                    </span>
                    <span class="font-weight-bold"
                            v-if="!!createdOrder['change_from']"
                            >
                            {{createdOrder['change_from']}}₽
                    </span>
                </div>
            </v-flex>
            <v-flex style="font-size: 16px; padding: 12px 16px;"
                    xs2 sm2 md2 lg2 xl2
                >
                <div>
                    Курьер позвонит, примерно, за час до прибытия
                </div>
            </v-flex>
            <v-flex style="font-size: 16px; padding: 12px 16px;" class=""
                    xs1 sm1 md1 lg1 xl1
                >
                <div style="text-align: center; font-size: 24px">
                    \ (•◡•) /
                </div>
            </v-flex>
            <v-flex style="font-size: 16px; padding: 0 16px 12px 16px"
                    xs2 sm2 md2 lg2 xl2
                >
                <div style="text-align: center">
                    Будем рады видеть вас снова
                </div>
            </v-flex>
            <v-flex text-xs-center
                    xs1 sm1 md1 lg1 xl1
                    class="headline"
                    style="padding: 0"
                    >
                <v-layout fill-height>
                    <v-flex align-self-end>
                        <v-btn flat
                                class="return-button"
                                style="margin:0; height:48px; width:100%;"
                                @click.stop="moveToCart"
                                >
                            Вернуться в корзину
                        </v-btn>
                    </v-flex>
                </v-layout>
            </v-flex>
            <v-flex
                    xs1 sm1 md1 lg1 xl1
                    style="font-size: 14px; color: #9e9e9e"
                    >
                <v-layout fill-height row style="padding: 12px 16px">
                    <v-flex style="">
                        <span style="color: #ffa559">*</span>
                    </v-flex>
                    <v-flex style="padding-left: 4px">
                        Внизу главной страницы есть кнопка "Контакты",
                        воспользуйтесь ей если возникнут вопросы
                    </v-flex>
                </v-layout>
            </v-flex>
        </v-layout>
    </v-container>
    <div v-show="!orderDialogShowed" style="padding: 0 16px">
        <v-toolbar flat class="cart-toolbar">
            <v-layout justify-center fill-height
                    class="icon-cart-container"
                    >
                <v-flex align-self-start text-xs-center>
                    <v-btn flat
                            @click="showNavigation = false"
                            >
                        <icon-cart
                               class="icon-cart"
                               width="16"
                               height="16"
                               ></icon-cart>
                        <h1 class="font-weight-regular text-uppercase">
                            ваш заказ
                        </h1>
                    </v-btn>
                </v-flex>
            </v-layout>
        </v-toolbar>
        <cart-view 
                ref="cartView"
                >
        </cart-view>

        <h3 class="cart-title subheading">Контакты</h3>
        <dual-field
                ref="contactsPair"
                >
            <template v-slot:top-field="{ focusTop, blurTop, inputTop }">
                <v-text-field solo flat hide-details
                        browser-autocomplete="name"
                        v-model="personName"
                        class="input-field body-1"
                        placeholder="Имя"
                        @focus="focusTop"
                        @blur="blurTop"
                        @input="inputTop"

                        :rules="[rules.required('Name is required')]"
                        ref="personName"
                        ></v-text-field>
            </template>
            <template
                    v-slot:bottom-field="{
                        focusBottom, blurBottom, inputBottom }"
                    >
                <input type="tel" autocomplete="on"
                        class="body-1 input-field person-phone"
                        v-model="purePhone"
                        v-mask="'+7 (###) ###-####'"
                        placeholder="Телефон"
                        @focus="focusBottom"
                        @blur="blurBottom"
                        @input="inputBottom"

                        ref="personPhone"
                        />
            </template>
        </dual-field>

        <h3 class="cart-title subheading">Доставка</h3>
        <dual-field>
            <template v-slot:top-field="{ focusTop, blurTop }">
                <Address
                    v-model="personAddress"
                    @focus="focusTop"
                    @blur="blurTop"

                    :rules="[rules.required('Address is required')]"
                    ref="personAddress"
                    ></Address>
            </template>
            <template v-slot:bottom-field="{ focusBottom, blurBottom }">
                <div class="delivery-group__menu-container">
                    <v-menu lazy offset-y
                            v-model="datePickerMenu"
                            :close-on-content-click="false"
                            :nudge-right="12"

                            transition="scale-transition"
                            attach=".date-picker"
                            >
                        <template v-slot:activator="{}">
                            <div
                                    class="date-picker
                                        font-weight-medium text-xs-center"
                                    @click="datePickerClick ({
                                        focusBottom, blurBottom })">
                                <span>{{ deliveryDateFormatted }}</span>
                                <v-icon>event</v-icon>
                            </div>
                        </template>
                        <v-date-picker no-title
                                color="#eae300"
                                v-model="deliveryDate"
                                @input="closeDatePickerMenu (blurBottom)"
                                :allowedDates="allowedDates"
                                locale="ru-ru"
                                >
                        </v-date-picker>
                    </v-menu>
                    <v-menu bottom offset-y
                            v-model="intervalSelectorMenu"
                            transition="scale-transition"
                            attach=".interval-selector"
                            >
                        <template v-slot:activator="{}">
                            <div
                                    class="interval-selector
                                        body-1 font-weight-medium"
                                    @click="intervalSelectorClick ({
                                        focusBottom, blurBottom })">
                                <span>{{ deliveryInterval }}</span>
                                <v-icon>access_time</v-icon>
                            </div>
                        </template>
                        <v-list>
                            <v-list-tile
                                    v-for="(item, index) in deliveryIntervalItems"
                                    :key="index"
                                    @click="intervalSelectorItemClick (item)"
                                    >
                                <v-list-tile-title>{{ item }}</v-list-tile-title>
                            </v-list-tile>
                        </v-list>
                    </v-menu>
                </div>
            </template>
        </dual-field>

        <h3 class="cart-title subheading">Оплата</h3>
        <dual-field
            :bottomVisible="changeShowed"
            >
            <template v-slot:top-field="{ focusTop, blurTop }">
                <v-select solo flat hide-details 
                        class="input-field payment-group
                               body-1 font-weight-medium"
                        color="#eae300"

                        :menu-props="{
                            'bottom': true,
                            'offset-y': true,}"

                        placeholder="Payment"
                        v-model="paymentType"
                        :items="paymentTypeItems"

                        @focus="focusTop"
                        @blur="blurTop"

                        attach=".payment-group"
                        >
                    <template v-slot:item="{ item }">
                        <v-icon
                                style="magrin-left: 12px; margin-right: 8px"
                                v-if="item === paymentTypeItems[1]"
                                width="20"
                                height="20"
                                >credit_card</v-icon>
                        <v-icon
                                style="magrin-left: 12px; margin-right: 8px"
                                v-if="item !== paymentTypeItems[1]"
                                width="20"
                                height="20"
                                >money</v-icon>
                        <div>{{ item }}</div>
                    </template>
                    <template v-slot:selection="{ item }">
                        <v-icon
                                style="magrin-left: 12px; margin-right: 8px"
                                v-if="item === paymentTypeItems[1]"
                                width="20"
                                height="20"
                                >credit_card</v-icon>
                        <v-icon
                                style="magrin-left: 12px; margin-right: 8px"
                                v-if="item !== paymentTypeItems[1]"
                                width="20"
                                height="20"
                                >money</v-icon>
                        <div class="font-weight-medium">{{item}}</div>
                    </template>
                </v-select>
            </template>
            <template v-slot:bottom-field="{ focusBottom, blurBottom }">
                <v-text-field solo flat hide-details
                        v-model="changeFrom"
                        class="input-field body-1 change-from"
                        placeholder="Сдача с ..."
                        type="number"

                        @focus="focusBottom"
                        @blur="blurBottom"
                        >
                </v-text-field>
            </template>
        </dual-field>

        <h3 class="cart-title subheading">Дополнительно</h3>
        <div class="extra-group">
            <v-checkbox solo flat hide-details
                    v-model="emailFlag"
                    label="Отправить детали заказа на e-mail"
                    color="#eae300"
                    class="font-weight-medium email-flag"
                    ></v-checkbox>
            <v-text-field solo flat hide-details
                browser-autocomplete="email"
                v-show="emailFlag"
                :class="['input-field', 'email', 'body-1', emailValidationClass]"
                placeholder="E-mail"
                v-model="personEmail"
                :rules="[rules.email('Invalid format')]"
                @blur="validateEmail"
                >
            </v-text-field>
            <v-checkbox solo flat hide-details
                    v-model="recallFlag"
                    label="Перезвонить для подтверждения заказа"
                    color="#eae300"
                    class="font-weight-medium email-flag"
                    ></v-checkbox>
        </div>
        <h3 class="cart-title subheading">Комментарии</h3>
        <v-textarea solo flat hide-details
                v-model="specialInstructions"
                class="comments"
                >
        </v-textarea>
        <div>
            <v-checkbox
                    v-model="acceptPolicy"
                    :class="['accept-policy', 'font-weight-medium',
                             policyValidationClass]"
                    color="#eae300"
                    class="accept-policy font-weight-medium"
                    style="display: inline-block"
                    >
            </v-checkbox>
            <div style="font-size: 14px; font-weight: 500; padding-top: 20px; margin-bottom: 12px">
                Принимаю 
                <a style="text-decoration: underline; color: black"
                        @click="openRoute('/deliveryPolicies.html')"
                        >
                    Соглашение об условиях доставки
                </a>
                и
                <a style="text-decoration: underline; color: black"
                        @click="openRoute('/confidentialPolicies.html')"
                        >
                    Политику обработки персональных данных
                </a>
            </div>
        </div>
        <v-layout justify-center>
            <v-btn flat dark
                    class="checkout"
                    color="#eae300"

                    @click.stop="checkout"
                    >
                Заказать
            </v-btn>
            </v-dialog>

        </v-layout>
        <v-layout justify-center
                v-show="errorOnlyPolicies"
                >
            <span class="validation-error-text">
                * Необходимо принять условия
            </span>
        </v-layout>
        <v-layout
                v-if="dateValidationError"
                >
            <span class="validation-error-text">
                * Доставка на следующий день возможна только при заказе до 20:00
            </span>
        </v-layout>
        <v-layout
                :class="[amountValidationError ? 'validation-error-text' : '']"
                v-if="amount < 700"
                style="margin-bottom: 12px"
                >
            <div style="text-align: center; width: 100%"
                    class="font-weight-medium">
                Минимальная сумма заказа 700₽
            </div>
        </v-layout>
    </div>
</v-container>
</template>
<script>
import utils from '../utils.js'
import Address from './address.vue'

import CartView from './cart_view.vue'
import DualField from './dual_field.vue'

import IconCart from './icons/icon_cart.vue'
import IconCreditCard from './icons/icon_credit_card.vue'

import { mapGetters, mapState, mapMutations } from 'vuex'
import { mask } from 'vue-the-mask'


export default {
    name: 'Cart',
    components: {
        Address,
        IconCart,
        IconCreditCard,
        CartView,
        DualField,
    },
    directives: {
        mask
    },

    data () {
        return {
            valid: true,

            today: undefined,
            datePickerMenu: false,
            deliveryBottomBlur: null,
            intervalSelectorMenu: false,

            changeShowed: true,

            rules: {
                required: text => v => !!v || text,
                fullPhone: text => v => (
                    !!v && v.length === 11) || text,
                email: text => v => utils.emailRegexp.test(v) || text
            },

            policyValidationClass: '',
            emailValidationClass: '',
            errorOnlyPolicies: false,
            orderDialogShowed: false,
            orderCreating: true,

            purePhone: undefined,
//          createdOrder: {id: 1, amount: 42.00, weight: 2.3, change_from:5000},
            createdOrder: null,
            dateValidationError: false,
            amountValidationError: false,
        }
    },

    created () {
        this.deliveryDate = this.defaultDate
    },
    mounted () {
        let self = this
        this.$refs.personPhone.validate = ()=>{
            return (
                self.rules.required('Phone is required')
                    (self.personPhone) === true
                &&
                self.rules.fullPhone('Wrong phone format')
                    (self.personPhone) == true
            )
        }
    },
    destroyed () {
    },

    methods: {
        ...mapMutations ('cart', [
            'setOrderDetails',
            'clearCartItems',
        ]),

        openRoute (route) {
            window.open(route, '_blank');
        },

        validateField(field) {
            if (!field.validate()) {
                if (field.$emit) {
                    field.$emit('blur', field)
                } else {
                    this.$refs.contactsPair.blurBottom(field)
                }
            }

            return field.validate()
        },

        validateEmail () {
            let isValid = this.emailFlag
                          ? utils.emailRegexp.test(this.personEmail)
                          : true
            this.emailValidationClass = isValid ? '' : 'email-validation-error'

            return isValid
        },

        validateCartItems () {
            return this.$refs.cartView.validate()
        },

        validateAmount () {
            this.amountValidationError = this.amount < 700

            return this.amount >= 700
        },

        validate () {
            let results = [
                this.validateField(this.$refs.personName),
                this.validateField(this.$refs.personPhone),
                this.validateField(this.$refs.personAddress),

                this.validatePolicy(),
                this.validateEmail(),
                this.validateCartItems(),
                this.validateAmount()
            ]
            let errorOnlyPolicies = undefined

            let result = results.reduce((result, value, idx) => {
                if (idx === 3) {
                    errorOnlyPolicies = errorOnlyPolicies === undefined ? !value
                                        : errorOnlyPolicies
                } else {
                    errorOnlyPolicies = !value ? false : errorOnlyPolicies 
                }

                return !value || !result ? false : result
            }, true)

            this.errorOnlyPolicies = errorOnlyPolicies

            return result
        },

        checkout () {
            ym(56913685, 'reachGoal', 'checkoutRequested')

            if (this.validate()) {
                ym(56913685, 'reachGoal', 'validationPassed')
                this.dateValidationError = false

                let timeout = false
                let request = false
                setTimeout(()=>{
                    timeout = true
                    if (request) {
                        this.orderCreating = false
                        if (this.dateValidationError) {
                            this.orderDialogShowed = false
                        }
                    }
                }, 900)
                fetch(`/api/order/create`, {
                    method: 'POST',
                    body: JSON.stringify({
                        "cart":this.$store.state.cart,
                        "summary":{
                            "amount":this.amount,
                            "weight":this.weight,
                            "count":this.items.length,
                        },
                    }),
                })
                .then(response => {
                    return response.json()
                })
                .then(result => {
                    request = true

                    if (result.error) {
                        if (result.error.today) {
                            this.dateValidationError = true
                            this.today = new Date(result.error.today)
                        } else {
                            this.amountValidationError = true
                        }
                    } else {
                        this.createdOrder = result.data
                        this.clearCartItems()
                        ym(56913685, 'reachGoal', 'orderCreated')
                    }

                    if (timeout) {
                        this.orderCreating = false
                        if (this.dateValidationError) {
                            this.orderDialogShowed = false
                        }
                    }
                })
                .catch(exp => {
                    console.log(exp)});

                this.orderDialogShowed = true
            }
        },

        moveToCart () {
            this.orderDialogShowed = false
            this.orderCreating = true
        },

        closeOrder () {
            if (this.isMobile) {
                this.showNavigation = false
                setTimeout(()=>this.moveToCart(), 100)
            } else {
                this.moveToCart()
            }

        },

        datePickerClick ({ focusBottom, blurBottom }) {
            this.datePickerMenu = !this.datePickerMenu
            this.deliveryBottomBlur = blurBottom


            if (this.datePickerMenu) {
                focusBottom ()
            } else {
                blurBottom ()
            }
        },

        closeDatePickerMenu (blur) {
            this.datePickerMenu = false
            blur ()
        },

        allowedDates (value) {
            let today = this.today && this.today > new Date() ? this.today
                        : new Date()
            today = new Date(
                    today.getFullYear(),
                    today.getMonth(),
                    today.getDate(),
                    0, 0, 0);

            let date = new Date(value)

            let diffTime = date.getTime() - today.getTime();
            let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays > 1 && diffDays < 8) {
                return true
            } else {
                return false
            }
        },

        intervalSelectorClick ({ focusBottom, blurBottom }) {
            this.intervalSelectorMenu = !this.intervalSelectorMenu
            this.deliveryBottomBlur = blurBottom
        },

        intervalSelectorItemClick (item, blur) {
            this.deliveryInterval = item
        },

        validatePolicy () {
            this.policyValidationClass = !this.acceptPolicy ?
                                             'policy-validation-error'
                                             : ''
            this.errorOnlyPolicies = this.acceptPolicy ? false
                                     : this.errorOnlyPolicies

            return !!this.acceptPolicy
        },
    },

    computed: {
        ...mapState('cart', [
            'items',
            'deliveryIntervalItems',
            'paymentTypeItems',
        ]),
        ...mapGetters('cart', [
            'count',
            'weight',
            'amount',
        ]),

        isMobile () {
            return this.$vuetify.breakpoint.width <= 1264
        },

        orderView () {
            let view = {}

            view.date = [
                    this.createdOrder["delivery_date"].split('-')[2],
                    this.createdOrder["delivery_date"].split('-')[1],
                    this.createdOrder["delivery_date"].split('-')[0].slice(-2),
                ].join('.')
            view.from = this.deliveryIntervalItems[
                    this.createdOrder['delivery_interval']].slice(2, 7)
            view.till = this.deliveryIntervalItems[
                    this.createdOrder['delivery_interval']].slice(11, 16)
            view.paymentType = this.paymentTypeItems[
                    this.createdOrder["payment_type"]].toLowerCase()
            view.changeFrom = this.createdOrder["change_from"]
                              ? ', сдача с ' : ''

            /*
            view = {
                date: '28.03.19',
                from: '12:00',
                till: '15:00',
                paymentType: this.paymentTypeItems[1].toLowerCase(),
                changeFrom: ', сдача с '
            }
            */

            return view
        },

        defaultDate () {
            let today = new Date ()
            let result = new Date (today)

            if (result.getHours() >= 20) {
                result.setDate (result.getDate() + 2)
            } else {
                result.setDate (result.getDate() + 1)
            }

            let tzoffset = result.getTimezoneOffset() * 60000
            let localISOTime = (new Date(result.getTime() - tzoffset))
                .toISOString().slice(0, -1)
            return localISOTime.split('T')[0]
        },
        deliveryDateFormatted () {
            if (this.deliveryDate) {
                let splittedDate = this.deliveryDate.split('-')

                return [splittedDate[2], splittedDate[1],
                    splittedDate[0].substr(-2)].join('.')
            } else {
                return ''
            }
        },

        personName: {
            get () {
                return this.$store.state.cart.personName
            },
            set (value) {
                this.$store.commit('cart/updatePersonName', value)
            },
        },

        personPhone: {
            get () {
                return this.$store.state.cart.personPhone
            },
            set (value) {
                this.$store.commit('cart/updatePersonPhone', value)
            },
        },

        personAddress: {
            get () {
                return this.$store.state.cart.personAddress
            },
            set (value) {
                this.$store.commit('cart/updatePersonAddress', value)
            },
        },

        personEmail: {
            get () {
                return this.$store.state.cart.personEmail
            },
            set (value) {
                if (this.emailValidationClass) {
                    this.validateEmail()
                }
                this.$store.commit('cart/updatePersonEmail', value)
            },
        },

        deliveryDate: {
            get () {
                return this.$store.state.cart.deliveryDate
            },
            set (value) {
                this.$store.commit('cart/updateDeliveryDate', value)
            },
        },

        deliveryInterval: {
            get () {
                return this.$store.state.cart.deliveryInterval
            },
            set (value) {
                this.$store.commit('cart/updateDeliveryInterval', value)
            },
        },

        paymentType: {
            get () {
                return this.$store.state.cart.paymentType
            },
            set (value) {
                this.$store.commit('cart/updatePaymentType', value)
            },
        },

        changeFrom: {
            get () {
                return this.$store.state.cart.changeFrom
            },
            set (value) {
                this.$store.commit('cart/updateChangeFrom', value)
            },
        },

        extraFlags: {
            get () {
                return this.$store.state.cart.extraFlags
            },
            set (value) {
                this.$store.commit('cart/updateExtraFlags', value)
            },
        },

        specialInstructions: {
            get () {
                return this.$store.state.cart.specialInstructions
            },
            set (value) {
                this.$store.commit('cart/updateSpecialInstructions', value)
            },
        },

        acceptPolicy: {
            get () {
                return this.$store.state.cart.acceptPolicy
            },
            set (value) {
                this.$store.commit('cart/updateAcceptPolicy', value)
                this.validatePolicy()
            },
        },

        showNavigation: {
            get () {
                return this.$store.state.showNavigation
            },
            set (value) {
                this.$store.commit('setShowNavigation', value)
            },
        },

        emailFlag: {
            get () {
                return this.extraFlags[0]
            },
            set (value) {
                let newFlags = this.extraFlags.slice()
                newFlags[0] = value
                this.extraFlags = newFlags

                if (!value) {
                    this.emailValidationClass = ''
                }
            },
        },

        recallFlag: {
            get () {
                return this.extraFlags[1]
            },
            set (value) {
                let newFlags = this.extraFlags.slice()
                newFlags[1] = value
                this.extraFlags = newFlags
            },
        },
    },
    watch: {
        purePhone () {
            if (!this.purePhone) {
                this.personPhone = null
            } else {
                this.personPhone = this.purePhone.match(/\d+/g).join('')
            }
        },

        datePickerMenu () {
            if (!this.datePickerMenu && this.deliveryBottomBlur) {
                this.deliveryBottomBlur ()
            }
        },

        intervalSelectorMenu () {
            if (!this.intervalSelectorMenu && this.deliveryBottomBlur) {
                this.deliveryBottomBlur ()
            }
        },

        paymentType () {
            this.changeShowed = this.paymentType === this.paymentTypeItems[0] ?
                                true : false
            this.changeFrom = this.changeFrom ? null : this.changeFrom
        },

        amount () {
            if (this.amount >= 700) {
               this.amountValidationError = false
            }
        }
    },
}
</script>
<style scoped lang="styl">
secondary_background_color = #fffff5
primary_yellow_color = #fffdbc

error_color = #ffc28f
error_color_focused = #ffa559
border_color = #f2f0b3
border_color_focused = #eae300

.icon-cart
    margin-right: 12px
.icon-cart-container
    margin-top-container: 10px

.cart-container > .container
    padding-top: 0

.cart-toolbar
    background-color: secondary_background_color

.return-button
    background-color: primary_yellow_color
    color: #424003
    border-radius: 0

.input-field
.input-field >>> .v-input__control
    min-height: 40px !important

.person-phone
    background-color: white
    width: 100%
    padding: 0 12px

    &:focus
        outline: none

    &::placeholder
        color: #9e9e9e
        opacity: 1


.delivery-group__menu-container
    overflow: hidden
    background-color: white

.date-picker
.interval-selector
    height: 40px

    cursor: pointer
    user-select: none
    float: left

    padding-top: 9px

    &:hover .v-icon
        color: #eae300

    & > *
        display: inline-block
        vertical-align: middle

    & span
        margin-right: 6px

.date-picker
    padding-left: 28px

    & >>> .v-picker__body
        width: unset !important

.interval-selector
    margin-left: 26px !important

    .v-menu__content
        background-color: white

.extra-group
    padding-left: 10px

    .v-input
        margin-top: 0
        padding-top: 8px
        padding-bottom: 0

    & >>> label
        font-size: 14px
        color: black !important
    & >>> .v-input__control:hover i
        caret-color: #eae300 !important
        color: #eae300 !important

.email
    margin-left: 3px
    margin-top: 4px !important
    padding-top: 0px !important
    border: 1px solid border_color
    border-radius: 2px

    &:hover
        border-color: border_color_focused

    &.email-validation-error
        border-color: error_color
        &:hover
            border-color: error_color_focused

.change-from
    & >>> input::-webkit-outer-spin-button
    & >>> input::-webkit-inner-spin-button 
        /* display: none; <- Crashes Chrome on hover */
        -webkit-appearance: none
        margin: 0
    & >>> input[type=number]
        -moz-appearance:textfield /* Firefox */

.accept-policy
    float: left
    & >>> label
        font-size: 14px
        color: black !important
    & >>> .v-input__control:hover i
        caret-color: #eae300 !important
        color: #eae300 !important

    &.policy-validation-error >>> i
        color: error_color !important
    &.policy-validation-error >>> .v-input__control:hover i
        caret-color: #eae300 !important
        color: error_color_focused !important

.comments
    border: 1px solid #f2f0b3
    border-radius: 2px

    &:hover
    &.v-input--is-focused
        border: 1px solid #eae300 !important

.cart-title
    margin-top: 28px
    color: rgba(0,0,0,0.54);

.checkout
    margin-top: 8px
    color:#344816 !important
    background-color: primary_yellow_color
    border: 1px solid border_color
    margin-bottom: 22px

.validation-error-text
    color: error_color_focused

.order-container
    height: 100%
    background-color: #fffef6

.order-dialog_order-creating-text
    padding-top: 24px
    padding-bottom: 48px
    font-size: 18px
.order-close-button
    border: 1px solid #c9e0a7
    background-color: #d9f2b3
    color: #344816 !important
</style>
