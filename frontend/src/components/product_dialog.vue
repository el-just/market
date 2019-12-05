<template>
    <v-card>
        <v-toolbar card flat style="position: fixed; width: 900px; z-index: 2">
            <v-toolbar-title>
                <v-text-field solo flat
                        class="name"
                        v-model="productModel.product.name"
                        label="Product name"
                        >
                </v-text-field>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items class="hidden-sm-and-down">
                <v-btn flat
                        @click="save">
                    save
                </v-btn>
                <v-btn flat>
                    delete
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>
        <v-card-text style="padding-top: 64px">
            <v-container>
                <v-layout row wrap>
                    <v-flex xs12 sm12 md4 lg4 xl4>
                        <v-img v-if="productModel.product.img"
                            :aspect-ratio="16/9"
                            :src="productModel.product.img"

                            @click="$refs.imageUpload.click()"
                            >
                        </v-img>
                        <v-responsive v-else
                            :aspect-ratio="16/9"
                            @click="$refs.imageUpload.click()"
                            >
                            <v-container fill-height>
                                <v-layout justify-center align-center>
                                    <v-icon 
                                            class="photo-placeholder"
                                            large>
                                        insert_photo
                                    </v-icon>
                                </v-layout>
                            </v-container>
                        </v-responsive>
                        <input
                            v-show="false"
                            ref="imageUpload"
                            type="file"
                            @change="imageUploaded" />
                        <v-text-field
                            label="Image link"
                            v-model="productModel.product.img">
                        </v-text-field>
                        <v-textarea solo flat
                            label="Description"
                            v-model="productModel.product.description">
                        </v-textarea>
                        <v-text-field
                            label="Country"
                            @blur="clearManufacturer"
                            v-model="productModel.manufacturer.name">
                        </v-text-field>

                    </v-flex>
                    <v-flex xs12 sm12 md8 lg8 xl8>
                        <v-text-field
                            label="Declensions 1"
                            v-model="productModel.entity.declensions[0]">
                        </v-text-field>
                        <v-text-field
                            label="Declensions 2,3,4"
                            v-model="productModel.entity.declensions[1]">
                        </v-text-field>
                        <v-text-field
                            label="Declensions 0,5,6,7,8,9,1x"
                            v-model="productModel.entity.declensions[2]">
                        </v-text-field>
                        <v-chip
                                v-for="(labelModel, idx) in productModel.labels"
                                :color="`${colors[idx]} lighten-3`"
                                label
                                small
                                >
                            {{ labelModel.label.name }}
                        </v-chip>
                        <v-menu bottom offset-y
                                class="labels-menu"
                                :nudge-right="12"
                                transition="scale-transition"
                                :close-on-content-click="false"
                                >
                            <template v-slot:activator="{on}">
                                <v-btn
                                        flat
                                        color="primary"
                                        class="mb-2"
                                        v-on="on"
                                        >
                                    labels
                                </v-btn>
                            </template>
                            <v-text-field
									append-icon="send"
									label="Add new label"
									v-model="newLabelName"
									@click:append="createLabel"
									>
                            </v-text-field>
                            <v-data-table
                                    class="labels-list"
                                    selectable
                                    hide-actions
                                    hide-headers
                                    active-class="primary--text"
                                    transition

                                    :items="labels"
                                    :total-items="labels.length"
									v-model="productModel.labels"
                                    item-key="label.entity_id"
                                    >
                                <template v-slot:items="props">
                                    <tr :active="props.selected" @click="props.selected = !props.selected">
                                        <td>
                                            <v-checkbox
                                                :input-value="props.selected"
                                                primary
                                                hide-details
                                            ></v-checkbox>
                                        </td>
                                        <td
                                                style="cursor: pointer"
                                                @click=""
                                                >
                                            {{ props.item.label.name }}
                                        </td>
                                    </tr>
                                </template>
                            </v-data-table>
                        </v-menu>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-card-text>
    </v-card>
</template>
<script>
import _ from 'lodash'
import Product from '../db/product.js'
export default {
    name: 'ProductDialog',
    components: {
    },

    props: ['model', 'labels'],

    data () {
        return {
            colors: ['green', 'purple', 'indigo', 'cyan', 'teal', 'orange'],
            labelsDialogShowed: false,
            file: undefined,
            offers: [],
			selectedLabels: [],
            productModel: Product(),
			newLabelName: undefined,
        }
    },

    created () {
    },
    destroyed () {
    }, 
    methods: {
        imageUploaded (e) {
            const files = e.target.files

            if(files[0] !== undefined) {
                if(files[0].name.lastIndexOf('.') <= 0) {
                    return
                }

                const fr = new FileReader ()
                fr.readAsDataURL(files[0])
                fr.addEventListener('load', () => {
                    this.productModel.product.img = fr.result
                    this.file = files[0]
                })
            } else {
                this.model.img = ''
            }
        },

        findLabel (labelIdx) {
            if (this.labels.length) {
                let item = _(this.labels)
                    .thru(function(coll) {
                        return _.union(coll, _.map(coll, 'children'));
                    })
                    .flatten()
                    .find({ entity_id: labelIdx })

                return item ? item["name"] : null
            }

            return null
        },

		createLabel (){
            fetch(`/api/label/read_or_create`, {
                method: 'POST',
                body: JSON.stringify({
					model:{
						label:{
							name:this.newLabelName,
						}
					}
				}),
            })
		},

        save () {
            let formData = new FormData()
            formData.append('models', JSON.stringify([this.productModel]))
            if (this.file) {
                formData.append('file', this.file)
            }

            fetch(`/api/product/update_or_create`, {
                method: 'POST',
                body: formData,
            })
        },
        clearManufacturer () {
            this.productModel.product.manufacturer_id = undefined
            this.productModel.manufacturer.id = undefined
        }
    },

    computed: {
    },
    watch: {
        model () {
            if (this.model) {
                this.productModel = this.model
            } else {
                this.productModel = Product()
            }
        }
    },
}
</script>
<style scoped lang="styl">
.photo-placeholder:hover
    cursor: pointer

.labels-menu-container
    background-color: white

    .v-menu__content
        position: static

.labels-list
    width: 400px
</style>
