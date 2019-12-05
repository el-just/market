import db from './root.js'

export function Offer () {
    return {
        offer: Object.assign({}, db.offers()),
        entity: Object.assign({}, db.entities()),
        products: [],
        formats: [],
    }
}

export function Format (parent_id) {
    let model = {
        offer: Object.assign({}, db.offers()),
        entity: Object.assign({}, db.entities()),
    }
    model["offer"]["parent_id"] = parent_id
    return model
}
