import db from './root.js'

export default function () {
    return {
        product: Object.assign({}, db.products()),
        entity: Object.assign({}, db.entities()),
        manufacturer: Object.assign({}, db.manufacturers()),
        labels: [],
    }
}
