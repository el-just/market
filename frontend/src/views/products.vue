<template>
    <v-container fluid>
		<v-flex ml-4 class="title">
    		<router-link to="/admin">cd ..</router-link>
		</v-flex>
        <v-dialog
                v-model="dialogShowed"
                max-width="900px"
                >
            <product-dialog
                    :model="activeModel"
                    :labels="labels"
                    ></product-dialog>
        </v-dialog>
        <v-btn
            dark
            color="primary"
            class="mb-2"

            @click="create"
            >
                Create
        </v-btn>
        <v-data-table
                hoverable
                hide-actions
                active-class="primary--text"
                :items="products"
                :total-items="products.length"
                >
            <template v-slot:items="{item}">
                <td
                        style="cursor: pointer"
                        @click="activeModel = item"
                        >
                    {{ item.entity.name }}
                </td>
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
import _ from 'lodash'

import ProductDialog from '../components/product_dialog.vue'

export default {
    name: 'Products',
    components: {
        ProductDialog,
    },

    data () {
        return {
            dialogShowed: false,
            activeModel: null,
            products: [],
            labels:[],
        }
    },

    created () {
        this.loadLabels();
        this.loadProducts();
    },

    methods: {
        create () {
            this.dialogShowed = true
        },
        loadProducts () {
            let self = this
            fetch(`/api/product/list`, {method: 'GET'})
                .then(response => {
                    return response.json()})
                .then(result => {
                    self.products = result || []})
                .catch(exp => {
                    console.log(exp)});
        },

        loadLabels () {
            let self = this
            fetch(`/api/label/list`, {method: 'GET'})
                .then(response => {
                    return response.json()})
                .then(result => {
                    self.labels = result})
                .catch(exp => {
                    console.log(exp)});
        },
    },

    computed: {
    },
    watch: {
        activeModel () {
            this.dialogShowed = this.activeModel ? true : false
        },

        dialogShowed () {
            this.activeModel = this.dialogShowed ? this.activeModel : null
        },
    }
}
</script>
<style scoped lang="styl">
.add-button
    display: none

.add-button:hover
    color: #1976d2

.v-treeview-node__root:hover
.v-treeview-node__leaf:hover
    .add-button
        display: inline-block
</style>
