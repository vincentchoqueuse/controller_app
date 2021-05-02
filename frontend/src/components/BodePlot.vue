<template>
<div class="row h-100 ">
    <div class="col-sm-3 sidebar h-100">
        <h2>Bode Response</h2>
        <div class="error">{{server_error}}</div>
        <hr>
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
                <label for="n" class="col-sm-2 col-form-label">n</label>
                <div class="col-sm-10">
                    <input type="number" class="form-control form-control-sm" id="n" v-model="n" aria-describedby="n" min="1" max="1000">
                </div>
            </div>
        </div>
        <hr>
        <div>
            <button class="btn btn-secondary btn-block" v-on:click=submit>New Plot</button>
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
            <Plotly :data="plot_list_bode" :autoResize=true :layout=layout class="custom_plot" />
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
                <tr v-for="(plot,index) in plot_list_bode" :key="index">
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
    data: function () {
        return {
            ShowPlot: true,
            n: 100,
            name : "bode",
            server_error : null,
            layout : {
                grid: {rows: 2,columns: 1},
                title: {text:' '},
                xaxis: {title: {text: 'angular frequency (rad/s)',}, type: 'log'},
                yaxis: {title: {text: 'Mag (dB)'}, anchor: 'y1'},
                yaxis2:{title: {text: 'Phase (deg)'}, anchor: 'y2'}
            },
        }
    },
    computed: {
        ...mapFields(['plot_list_bode','system_list','selected'])
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
                this.server_error = null,
                this.$store.commit('add_bode_data',data);
            }
        },
        delete_plot(index)
        {
            this.plot_list_bode.splice(index,1);
        },
        submit(){
                var url = "https://g4feuj0638.execute-api.eu-west-1.amazonaws.com/test";
                var data = this.system_list[this.selected];
                var extra_data = { plot_type: "bode", n : this.n};
                data = Object.assign({}, data, extra_data);

                fetch(url, { method: 'POST',body: JSON.stringify(data),headers: {'Content-Type': 'application/json',}})
                .then(response => response.json()).then(data =>{this.add_plot_list(data);})
                .catch((error) => {alert('Error:', error);});
        }
    }
}

</script>

<style scoped>
</style>


