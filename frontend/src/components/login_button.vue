<template>
    <v-menu
            v-model="opened"
            :close-on-content-click="false"
            :nudge-width="200"
            offset-y
            content-class="menu-wrapper"
            >
        <template v-slot:activator="{ on }">
            <v-btn flat icon
                    class="user-button"
                    v-on="on"
                    >
                <icon-user
                       width="26"
                       height="26"
                       />
            </v-btn>
        </template>

        <v-container
                class="menu-container"
                >
            <v-card flat>
                <dual-field v-if="!auth"
                        class="login-pair"
                        borderColor="#d3f0fb"
                        borderColorFocused="#a0ddf5"
                        ref="loginPair"
                        >
                    <template
                            v-slot:top-field="{ focusTop, blurTop, inputTop }"
                            >
                        <input type="tel" autocomplete="on"
                                class="body-1 login-pair_tel-input"
                                v-model="login"
                                v-mask="'+7 (###) ###-####'"
                                placeholder="Телефон"
                                @focus="focusTop"
                                @blur="blurTop"
                                @input="inputTop"

                                @keyup.enter="$refs.password.focus"
                                ref="login"
                                />
                    </template>
                    <template v-slot:bottom-field="{
                            focusBottom, blurBottom, inputBottom }">
                        <v-text-field solo flat hide-details
                                v-model="password"
                                class="body-1 login-pair_password"
                                placeholder="Пароль"
                                @focus="focusBottom"
                                @blur="blurBottom"
                                @input="inputBottom"

                                @keyup.enter="enter"

                                type="password"
                                ref="password"
                                :rules="[
                                    rules.required('Password is required'),
                                    ]"
                                ></v-text-field>
                    </template>
                </dual-field>
                <v-layout v-if="!auth" justify-center wrap>
                    <v-flex text-xs-center 
                            xs12 sm12 md12 lg12 xl12
                            >
                        <v-btn flat dark
                               class="checkout"
                               color="rgb(71, 188, 234)"
                               @click="enter"
                               >
                            Войти
                        </v-btn>
                    </v-flex>
                    <v-flex v-if="badLogin"
                            text-xs-center
                            xs12 sm12 md12 lg12 xl12
                            style="position: absolute;
                                   bottom: -4px;
                                   font-size: 12px;
                                   color: #ffa559"
                            >
                        Пользователь не найден
                    </v-flex>
                </v-layout>
                <v-layout wrap
                        v-if="auth"
                        class="authed-menu"
                        >
                    <v-flex text-xs-center
                            xs12 sm12 md12 lg12 xl12
                            style="padding-top: 32px; padding-bottom: 48px;
                                   color: #9e9e9e"
                            class="font-weight-medium"
                            >
                        Скоро здесь будет много всего интересного +)
                    </v-flex>
                    <v-flex text-xs-right>
                        <a @click="logout">выйти</a>
                    </v-flex>
                </v-layout>
            </v-card>
        </v-container>
    </v-menu>
</template>
<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

import IconUser from './icons/icon_user.vue'
import DualField from './dual_field.vue'
import { mask } from 'vue-the-mask'

export default {
    name: 'LoginButton',
    components: {
        IconUser,
        DualField,
    },
    directives: {
        mask
    },

    props: [],
    data () {
        return {
            opened: false,
            login: null,
            password: null,
            rules: {
                required: text => v => !!v || text,
                fullPhone: text => v => ( !!v && v.length === 11 )
                                        || text,
            },

            badLogin: false,
        }
    },

    created () {
    },
    mounted () {
        let self = this
        this.$refs.login.validate = ()=>{
            return (
                self.rules.required('Phone is required')
                    (self.pureLogin) === true
                &&
                self.rules.fullPhone('Wrong phone format')
                    (self.pureLogin) == true
            )
        }
    },
    destroyed () {
    },

    methods: {
        ...mapMutations('user', [
                'setAuth'
        ]),

        validateField(field) {
            if (!field.validate()) {
                if (field.$emit) {
                    field.$emit('blur', field)
                } else {
                    this.$refs.loginPair.blurTop(field)
                }
            }

            return field.validate()
        },

        enter () {
            let self = this
            if ((this.validateField(this.$refs.login) &
                    this.validateField(this.$refs.password)) === 1) {
                fetch(`/api/user/login`, {
                        method: 'POST',
                        credentials: 'include',
                        body: JSON.stringify({
                            login: this.pureLogin,
                            password: this.password,
                        }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => {
                        return response.json()
                    })
                    .then(result => {
                        if (result.success) {
                            this.opened = false
                            this.badLogin = false
                            this.password = null
                            setTimeout(()=>{this.setAuth(true)}, 150)
                        } else {
                            this.badLogin = true
                        }
                    })
                    .catch(exp => {
                        console.error(exp)});
            }
        },

        logout () {
            fetch(`/api/user/logout`, {
                    method: 'GET',
                    credentials: 'include',
                })
                .then(response => {
                    return response.json()
                })
                .then(result => {
                    this.opened = false
                    setTimeout(()=>{this.setAuth(false)}, 150)
                })
                .catch(exp => {
                    console.error(exp)});
        },
    },

    computed: {
        ...mapState('user', [
            'auth'
        ]),

        pureLogin() {
            if (!this.login) {
                return null
            } else {
                return this.login.match(/\d+/g).join('')
            }
        }
    },
    watch: {
        opened () {
            if (this.opened && !this.auth) {
                setTimeout(()=>this.$refs.login.focus(), 200)
            }
        }
    },
}
</script>
<style scoped lang="styl">

.menu-container
    background-color: white
    padding: 12px

.authed-menu
    a
        color: #9e9e9e
        &:hover
            text-decoration: underline
.login-pair
    margin: 12px 12px 0 12px

    .login-pair_tel-input
        height: 40px
        padding: 0 12px
        &:focus
            outline: none

        &::placeholder
            color: #9e9e9e
            opacity: 1

    .login-pair_password >>> .v-input__control
        min-height: 40px
</style>
