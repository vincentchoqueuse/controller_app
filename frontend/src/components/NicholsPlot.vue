<template>
<div class="row h-100 ">
    <div class="col-sm-3 sidebar h-100">
        <h2>Nichols Chart</h2>
        <div class="error">{{server_error}}</div>
        <hr>
        <h3>Grid</h3>
        <div class="side">
            <div class="form-group row">
                <label for="cmag" class="col-sm-2 col-form-label">Gain</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control form-control-sm" id="name" v-model="grid_nichols" aria-describedby="name">
                </div>
            </div>
        </div>
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
                    <input type="number" class="form-control form-control-sm" id="n" v-model="n" aria-describedby="n" >
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
                <tr v-for="(plot,index) in plot_list_nichols" :key="index">
                   <th>{{ index+ 1}}</th>
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
            server_error : null,
            ShowPlot: true,
            name : "plot",
            n: 100,
            plot_contours : [],
            layout : {
                hovermode : 'closest',
                title: {text:' '},
                xaxis: {title: {text: 'Phase (deg)',}},
                yaxis: {title: {text: 'Mag (dB)'}},
            }
        }
    },
    created: function () {
        this.plot_contours = this.compute_contours();
    },
    watch: {
        grid_nichols: function() {
        this.plot_contours = this.compute_contours();
        }
    },
    computed: {
        ...mapFields(['plot_list_nichols','system_list','selected','grid_nichols']),
        plot_data: function()
        {
            var data = this.$store.state.plot_list_nichols;
            data = data.concat(this.plot_contours);
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
                this.$store.commit('add_nichols_data',data);
            }
        },
        delete_plot(index)
        {
            this.plot_list_nichols.splice(index,1);
        },
        compute_contours: function ()
        {
            var values = this.grid_nichols.split(",");
            var data = [];
            for (var i=0;i<values.length;i++)
            {
                var M =Math.pow(10,values[i]/20);
                var name = values[i]+" dB";
                var x,x_temp,x_old=-360;
                var y ;
                var angle = 0;
                var N = 1000;
                var x_data = [];
                var y_data = [];
                for (var indice=0;indice<N;indice++)
                    {
                    if (M==1)
                    {
                        x = -0.5;
                        y = 60*2*(indice-N/2)/N;
                    }
                    else{
                        angle = 2*Math.PI*indice/N;
                        x = (M/(1-M*M))*Math.cos(angle)+(M*M/(1-M*M));
                        y = (M/(1-M*M))*Math.sin(angle);
                    }
                    x_temp = Math.atan2(y,x)*180/Math.PI
                    if ((x_temp-x_old)>300)
                    {
                        x_temp = x_temp-360;
                    }
                    if ((x_temp-x_old)<-300)
                    {
                        x_temp = x_temp+360;
                    }
                    x_old = x_temp;
                    y_data.push(10*Math.log10(x*x+y*y));
                    x_data.push(x_temp);
                    }
                data.push({x:x_data,y:y_data,hoverinfo:'name',name: name,  showlegend:false, line:{color:'#555', width:'1', dash:'dot'}});
            }
            return data;
        },
        submit(){
                var url = "https://g4feuj0638.execute-api.eu-west-1.amazonaws.com/test";
                var data = this.system_list[this.selected];
                var extra_data = { plot_type: "nichols", n : this.n};
                data = Object.assign({}, data, extra_data);

                fetch(url, { method: 'POST',body: JSON.stringify(data),headers: {'Content-Type': 'application/json',}})
                .then(response => response.json()).then(data =>{this.add_plot_list(data);})
                .catch((error) => {this.server_error=error;});
        }
    }
}

</script>

<style scoped>
</style>


