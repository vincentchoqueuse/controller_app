import Vue from 'vue'
import Vuex from 'vuex'
import {getField,updateField} from 'vuex-map-fields';


Vue.use(Vuex)

export default new Vuex.Store({
   state: {
    url : "https://g4feuj0638.execute-api.eu-west-1.amazonaws.com/test",
    plot_list_time: [],
    plot_list_bode: [],
    plot_list_nichols: [] ,
    plot_list_zpmap: [] ,
    selected : 0,
    system_list: [{name : "system1",controller_Cl: false,controller_Ki : "1",controller_Ti: "1", controller_type: "none", sys_num : "1", sys_den : "1,1,1",sys_Ts: "1", sys_type: "continuous"}],
  },
  getters: {
    getField,
  },
  mutations: {
    updateField,
    change_selected(state,index)
    {
        if (index==-1)
            {
            index = state.system_list.length-1;
            }
        state.selected = index;
    },
    add_system(state,data)
    {
        state.system_list.push(data);
    },
    add_time_data(state,data)
        {
        state.plot_list_time.push(data);
        },
    add_bode_data(state,data)
        {
        state.plot_list_bode.push(data[0]);
        state.plot_list_bode.push(data[1]);
        },
    add_nichols_data(state,data)
        {
        state.plot_list_nichols.push(data);
        },
    add_zpmap_data(state,data)
        {
        state.plot_list_zpmap.push(data[0]);
        state.plot_list_zpmap.push(data[1]);
        }
    },
}                              
);



