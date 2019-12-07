<template>
    <v-container>
        <v-layout>
            <v-flex text-xs-center>
                <v-btn
                        :color="stage === 'production' ? 'warning' : 'success'"
                        @click="toggleStage"
                        >
                    {{ stage === 'production' ? 'To Test' : 'To Production' }}
                </v-btn>
            </v-flex>
        </v-layout>
        <v-layout>
            <v-flex text-xs-center class="title">
                <router-link to="/admin/products">Products</router-link>
            </v-flex>
            <v-flex text-xs-center class="title">
                <router-link to="/admin/offers">Offers</router-link>
            </v-flex>
            <v-flex text-xs-center class="title">
                <router-link to="/admin/sales">Sales</router-link>
            </v-flex>
        </v-layout>
    </v-container>
</template>
<script>
export default {
    name: 'admin',
    components: {
    },

    props: [],
    data () {
        return {
        }
    },

    created () {
    },
    destroyed () {
    },

    methods: {
        toggleStage () {
            let stageTo = this.stage === 'production' ? 'test' : 'production'

            fetch('/api/market/set_stage', {
                    method: 'POST',
                    credentials: 'include',
                    body: JSON.stringify({stage: stageTo}),
                })
                .then(response => {
                    return response.json()
                })
                .then(result => {
                    this.stage = stageTo
                })
        },
    },

    computed: {
        stage: {
            get () {
                return this.$store.state.stage
            },
            set (value) {
                this.$store.commit('setStage', value)
            },
        },
    },
    watch: {
    },
}
</script>
<style scoped lang="styl">
</style>
