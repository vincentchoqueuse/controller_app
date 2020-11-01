import Vue from 'vue'
import Router from 'vue-router'
import Systems from '@/components/Systems'
import BodePlot from '@/components/BodePlot'
import NicholsPlot from '@/components/NicholsPlot'
import TimePlot from '@/components/TimePlot'
import ZPPlot from '@/components/ZPPlot'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Systems
    },
    {
      path: '/system',
      name: 'System',
      component: Systems
    },
    {
      path: '/step',
      name: 'Time Plot',
      component: TimePlot
    },
    {
      path: '/bode',
      name: 'Bode Plot',
      component: BodePlot
    },
    {
      path: '/nichols',
      name: 'Nichols Plot',
      component: NicholsPlot
    },
    {
    path: '/zpmap',
    name: 'Poles Zeros Map',
    component: ZPPlot
    }
  ]
})
