<template>
    <div class="address-container">
        <v-menu
                bottom offset-y
                attach=".address-container"
                v-model="autocompleteVisible">
            <template v-slot:activator="{ autocompleteVisible }">
                <v-textarea solo flat hide-details
                    browser-autocomplete="street-address"
                    class="address-area body-1"
                    :placeholder="'Адрес в Санкт-Петербурге (по области '
                                   + 'пока не работаем)'"
                    @focus="focus"
                    @blur="blur"

                    rows="2"

                    ref="addressField"

                    v-model="baseAddress"
                    :rules="rules"
                    ></v-textarea>
            </template>
            <v-list style="background-color: white">
                <v-list-tile
                    v-for="(item, index) in autocompleteItems"
                    :key="index"
                    @click="addressClick(item)"
                    >
                    <v-list-tile-title>
                        {{ stringifyItem(item) }}
                    </v-list-tile-title>
                </v-list-tile>
            </v-list>
        </v-menu>
    </div>
</template>
<script>
import _ from 'lodash'


let debounceInterval = 300
export default {
    name: 'Address',
    components: {
    },

    props: ['rules'],
    data () {
        return {
            autocompleteVisible: false,
            baseAddress: null,
            autocompleteItems: [],
        }
    },

    created () {
    },
    destroyed () {
    },

    methods: {
        requestAddressList: _.debounce((baseAddress, self)=> {
            fetch(`/api/address/list?search_text=${baseAddress}`,
                    {method: 'GET'})
                .then(response => {
                    return response.json()
                    })
                .then(result => {
                    self.autocompleteVisible = !!result.length
                    if (result.length === 1) {
                        if (result[0].unrestricred_value.indexOf(
                                self.baseAddress) !== -1) {
                            result = []
                        }
                    }

                    if (self.autocompleteVisible) {
                        self.autocompleteItems = result
                    } else {
                        setTimeout(()=>{
                            self.autocompleteItems = result}, 100)
                    }
                    })
                .catch(exp => {
                    self.autocompleteVisible = false
                    self.autocompleteItems = []
                    });
        }, debounceInterval),

        addressClick (item) {
            this.baseAddress = this.stringifyItem(item)

            this.$refs.addressField.focus()
        },

        stringifyItem (item) {
            let data = []

            data.push(item.data.street_with_type)
            if (item.data.house) {
                let block_data = item.data.block
                        ? ` ${item.data.block_type} ${item.data.block}`: ''

                data.push(
                    `${item.data.house_type} ${item.data.house}${block_data}`)
            }

            return data.join(', ')
        },

        focus () {
            this.$emit('focus')
        },
        blur () {
            this.$emit('blur')
        },
        validate () {
            return this.$refs.addressField.validate()
        },
    },

    computed: {
    },
    watch: {
        baseAddress (baseAddress) {
            if (this.autocompleteItems.filter(item => {
                    return this.stringifyItem(item) === this.baseAddress
                    }).length === 0) {
                this.requestAddressList(baseAddress, this)
            }

            this.$emit('input', this.baseAddress)
        }
    },
}
</script>
<style lang="styl">
    .address-area
        textarea
            resize: none
            margin-top: 0 !important
            padding-top: 10px
</style>
