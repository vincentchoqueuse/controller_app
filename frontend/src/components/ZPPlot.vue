<template>
<div class="row h-100 ">
    <div class="col-sm-3 sidebar h-100">
        <h2>Poles and Zeros Map</h2>
        <div class="error">{{server_error}}</div>
        <h3>Additional Grid</h3>
        <div class="side">
            <div class="form-group row">
                <label for="cmag" class="col-sm-2 col-form-label">Circle</label>
                <div class="col-sm-10">
                    <div class="custom-control custom-checkbox">
                      <input type="checkbox" class="custom-control-input" id="circle" v-model="circle" >
                      <label class="custom-control-label" for="circle">Show</label>
                    </div>
                </div>
            </div>
        </div>
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
            <Plotly :data="plot_data" :autoResize=true :layout=layout class="custom_plot" />
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
                <tr v-for="(plot,index) in plot_list_zpmap" :key="index">
                   <th>{{ index+1 }}</th>
                   <td>{{ plot.name }}</td>
                    <td><input type="color" class="form-control form-control-sm btn-color" id="favcolor" name="favcolor" :value=plot.line.color disabled></td>
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
            ShowPlot: true,
            circle : true,
            server_error : null,
            plot_circle : [],
            layout : {
                hovermode : 'closest',
                title: {text:' '},
                xaxis: {title: {text: 'Real Part',},},
                yaxis: {title: {text: 'Imaginary Part'},scaleanchor:"x",scaleratio:1}
            }
        }
    },
    created: function () {
            this.plot_circle = this.compute_circle();
    },
    watch: {
        circle: function() {
            this.plot_circle = this.compute_circle();
        }
    },
    computed: {
            ...mapFields(['system_list','plot_list_zpmap','selected']),
            plot_data: function()
            {
                var data = this.$store.state.plot_list_zpmap;
                data = data.concat(this.plot_circle);
                return data;
            }
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
                this.$store.commit('add_zpmap_data',data);
            }
        },
        delete_plot(index)
        {
            this.plot_list_zpmap.splice(index,1);
        },
        compute_circle: function ()
        {
            var data = []
            if (this.circle == true)
                {
                var angle;
                var x = [];
                var y = [];
                for (var i=0;i<300;i++)
                    {
                    angle = 2*Math.PI*i/300.;
                    x.push(Math.cos(angle));
                    y.push(Math.sin(angle));
                    }
                data=[{x:x,y:y,showlegend:false, line:{color:'#555', width:'1', dash:'dot'}}];
                }
            return data;
        },
        submit(){
                var url = "https://g4feuj0638.execute-api.eu-west-1.amazonaws.com/test";
                var data = this.system_list[this.selected];
                var extra_data = { plot_type: "zpmap"};
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



