<template>
<div class="row h-100 ">
    <div class="col-sm-3 sidebar h-100">
        <h2>Time Response</h2>
        <div class="error">{{server_error}}</div>
        <h3>Add Plot</h3>
        <div class="side">
            <div class="form-group row">
                <label for="name" class="col-sm-2 col-form-label">name</label>
                <div class="col-sm-10">
                <select v-model=selected class="custom-select custom-select-sm">
                    <option v-for="(item, key) in system_list" :value="key" :key="key">
                        {{item.name}}
                    </option>
                </select>
                </div>
            </div>
            <div class="form-group row">
                <label for="Type" class="col-sm-2 col-form-label">Input</label>
                <div class="col-sm-10">
                    <select class="custom-select custom-select-sm" v-model="input_type" v-on:change="change_input_type">
                        <option value="step">Step</option>
                        <option value="impulse">Impulse</option>
                        <option value="sine">Sinewave</option>
                    </select>
                </div>
            </div>
            <div class="form-group row">
                <label for="input_f0" class="col-sm-2 col-form-label">f0</label>
                <div class="col-sm-10">
                    <input type="number" class="form-control form-control-sm" id="input_f0" v-model="input_f0" aria-describedby="f0" :disabled="f0_disabled">
                </div>
            </div>
            <div class="form-group row">
                <label for="input_a0" class="col-sm-2 col-form-label">Amp</label>
                <div class="col-sm-10">
                    <input type="number" class="form-control form-control-sm" id="input_a0" v-model="input_a0" aria-describedby="a0">
                </div>
            </div>
            <div class="form-group row">
                <label for="N" class="col-sm-2 col-form-label">N</label>
                <div class="col-sm-10">
                    <input type="number" class="form-control form-control-sm" id="N" v-model="N" aria-describedby="N" min="1" max="1000">
                </div>
            </div>
            <div>
                 <button class="btn btn-secondary btn-block" v-on:click=submit>Plot</button>
            </div>
        </div>  
    </div>
    <div class="col-sm-9">
        <div class="menu">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class="nav-link" href="#" :class="{ 'active' : ShowPlot}" @click="ShowPlot=true">Figures</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#" :class="{ 'active' : !ShowPlot}" @click="ShowPlot=false">List</a>
                </li>
            </ul>
        </div>
        <div v-if='ShowPlot' class="h-100">
            <Plotly :data="plot_list_time" :autoResize=true :layout=layout class="custom_plot" />
        </div>
        <div v-show='!ShowPlot' class="h-100">
              <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Color</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(plot,index) in plot_list_time" :key="index">
                   <th>{{ index+1 }}</th>
                   <td>{{ plot.name  }}</td>
                    <td><div class="badge badge-color" v-bind:style="{ backgroundColor: plot.line.color }">{{plot.line.color}}</div></td>
                   <td><button @click="delete_plot(index)" class="btn btn-sm btn_simple"><font-awesome-icon icon="trash" /></button></td>
                </tr>
               </tbody>
            </table>
        </div>
    </div>
</div>
</template>

<script>
import { mapFields } from 'vuex-map-fields';
import {Plotly} from 'vue-plotly'

export default {
    name: 'System',
    components: {Plotly},
    data : function()
        {
        return {
            input_f0 : 1.0,
            input_a0 : 1.0,
            input_type : "step",
            ShowPlot: true,
            N: 100,
            server_error : null,
            f0_disabled : true,
            layout : {
                title: {text:' '},
                xaxis: {title: {text: 'time (s)',},},
                yaxis: {title: {text: 'Step Response'},}
            }
        }
    },
    computed: {
            ...mapFields(['system_list','plot_list_time','selected'])
    },
    methods: {
        add_plot_list(data)
        {
            if (data["error"])
            {
                this.server_error = data["error"];
            }
            else
            {
                this.server_error = null;
                this.$store.commit('add_time_data',data);
            }
        },
        change_input_type(){
            var values = {"sinewave":false,"step":true,"impulse":true};
            this.f0_disabled = values[this.input_type];
        },
        delete_plot(index)
        {
            this.plot_list_time.splice(index,1);
        },
        submit(){
                var url = "https://g4feuj0638.execute-api.eu-west-1.amazonaws.com/test";
                var data = this.system_list[this.selected];

                var extra_data = { plot_type: "time", N : this.N, extra: {type: this.input_type,a0: this.input_a0,f0:this.input_f0} };
                data = Object.assign({}, data, extra_data);
                fetch(url, { method: 'POST',body: JSON.stringify(data),headers: {'Content-Type': 'application/json',}})
                .then(response => response.json()).then(data =>{this.add_plot_list(data)})
                .catch((error) => {console.log(error);});
        }
    }
}
</script>

<style scoped>

</style>


