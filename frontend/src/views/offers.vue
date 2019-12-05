<template>
    <v-container fluid>
        <v-flex ml-4 class="title">
            <router-link to="/admin">cd ..</router-link>
        </v-flex>
        <v-dialog
                v-model="dialogShowed"
                max-width="900px"
                >
            <offer-dialog
                    :model="activeModel"
                    :products="products"
                    ></offer-dialog>
        </v-dialog>
        <v-btn
            dark
            color="primary"
            class="mb-2"

            @click="create"
            >
               create 
        </v-btn>
        <v-btn
            class="mb-2"
            @click="$refs.jsonUpload.click()"
            >
               Import 
        </v-btn>
        <v-btn
            class="mb-2"
            @click="exportOffers"
            >
                Export
        </v-btn>
        <input
                v-show="false"
                ref="jsonUpload"
                type="file"
                @change="jsonUploaded"
                />
        <v-data-table
                hoverable
                hide-actions
                active-class="primary--text"
                :items="offers"
                :total-items="offers.length"
                >
            <template v-slot:items="{item}">
                <td
                        style="cursor: pointer"
                        @click="activeModel = item"
                        >
                    {{ item.offer.name }}
                </td>
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
import _ from 'lodash'
import OfferDialog from '../components/offer_dialog.vue'

export default {
    name: 'Offers',
    components: {
        OfferDialog,
    },

    data () {
        return {
            dialogShowed: false,
            activeModel: null,
            offers: [],
            products: [],
        }
    },

    created () {
        this.loadOffers();
        this.loadProducts();
    },

    methods: {
        create () {
            this.dialogShowed = true
        },
        loadOffers () {
            let self = this
            fetch(`/api/market/list?category=0&paused=true`, {method: 'GET'})
                .then(response => {
                    return response.json()})
                .then(result => {
                    self.offers = result || []})
                .catch(exp => {
                    console.log(exp)});
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

        jsonUploaded (event) {
            const files = event.target.files

            if(files[0] !== undefined) {
                if(files[0].name.lastIndexOf('.') <= 0) {
                    return
                }

                const fr = new FileReader ()
                fr.readAsDataURL(files[0])
                fr.addEventListener('load', () => {
                    let formData = new FormData()
                    formData.append('file', files[0])
                    fetch(`/api/offer/load`, {
                        method: 'POST',
                        body: formData,
                    })
                })
            }
        },

        exportOffers () {
            let element = document.createElement('a');
            element.setAttribute(
                'href',
                'data:text/plain;charset=utf-8,' + encodeURIComponent(
                    JSON.stringify(this.offers)));
            element.setAttribute('download', 'offers.json');

            element.style.display = 'none';
            document.body.appendChild(element);

            element.click();

            document.body.removeChild(element);
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
</style>
