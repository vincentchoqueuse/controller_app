import Vue from 'vue'
import App from './App.vue'
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/main.css';
import store from './store'
import { library } from '@fortawesome/fontawesome-svg-core'
import {faTrash,faUserSecret,faCog,faClone,faPlus,faPoll} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import router from './router'

library.add(faUserSecret,faCog,faClone,faPlus,faPoll,faTrash)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

new Vue({
        render: h => h(App),
        store: store,
        router :  router,
}).$mount('#app')

