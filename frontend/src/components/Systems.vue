<template>
<div class="row h-100 ">
    <div class="col-sm-3 sidebar h-100">
        <h2>System Parameters</h2>
        <div class="error">{{server_error}}</div>
        <h3>System</h3>
        <div class="form-group row">
            <label for="name" class="col-sm-2 col-form-label">name</label>
            <div class="col-sm-10">
                <input type="text" class="form-control form-control-sm" id="name" v-model="name" aria-describedby="name" >
            </div>
        </div>
        <div class="form-group row">
            <label for="N" class="col-sm-2 col-form-label">Color</label>
            <div class="col-sm-10">
                <input type="color" class="form-control form-control-sm" id="favcolor" name="favcolor" v-model="color">
            </div>
        </div>
        <div class="form-group row">
            <label for="Type" class="col-sm-2 col-form-label">Type</label>
            <div class="col-sm-10">
                <select class="custom-select custom-select-sm" v-model="sys_type" v-on:change="change_system_type">
                    <option >continuous</option>
                    <option >discrete</option>
                </select>
            </div>
        </div>
        <div class="form-group row">
            <label for="num" class="col-sm-2 col-form-label">Num</label>
            <div class="col-sm-10">
                <input type="text" class="form-control form-control-sm" id="num" v-model="sys_num" aria-describedby="emailHelp">
            </div>
        </div>
        <div class="form-group row">
            <label for="num" class="col-sm-2 col-form-label">Den</label>
            <div class="col-sm-10">
                <input type="text" class="form-control form-control-sm" id="den" v-model="sys_den" aria-describedby="emailHelp">
            </div>
        </div>
        <div class="form-group row">
            <label for="Ts" class="col-sm-2 col-form-label">Ts</label>
            <div class="col-sm-10">
                <input type="number" class="form-control form-control-sm" id="Ts" v-model="sys_Ts" aria-describedby="Ts" :disabled="Ts_disabled == 1">
            </div>
        </div>
        <h3 >Controller</h3>
        <div class="form-group row">
            <label class="col-sm-2 col-form-label">Loop</label>
            <div class="col-sm-10">
                <div class="custom-control custom-switch">
                    <input type="checkbox" class="custom-control-input" id="customSwitch1" v-model="controller_Cl">
                    <label class="custom-control-label" for="customSwitch1">{{show_loop}}</label>
                </div>
            </div>
        </div>
        <div class="form-group row">
            <label for="Type" class="col-sm-2 col-form-label">Type</label>
            <div class="col-sm-10">
                <select class="custom-select custom-select-sm" v-model="controller_type" v-on:change="change_controller_type">
                    <option >none</option>
                    <option >P</option>
                    <option >PI</option>
                </select>
            </div>
        </div>
        <div class="form-group row">
            <label for="Ki" class="col-sm-2 col-form-label">Ki</label>
            <div class="col-sm-10">
                <input type="number" class="form-control form-control-sm" id="Ki" v-model="controller_Ki" aria-describedby="Ki" :disabled="Ki_disabled == 1">
            </div>
        </div>
        <div class="form-group row">
            <label for="Ti" class="col-sm-2 col-form-label">Ti</label>
            <div class="col-sm-10">
                <input type="number" class="form-control form-control-sm" id="Ti" v-model="controller_Ti" aria-describedby="Ti" :disabled="Ti_disabled == 1">
            </div>
        </div>
        <div>
            <button class="btn btn-secondary btn-block" v-on:click=submit>Save</button>
        </div>
    </div>
    <div class="col-sm-9">
        <div class="menu">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class="nav-link active" href="#">System List</a>
                </li>
            </ul>
            <div>
              <table class="table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>name</th>
                  <th>color</th>
                  <th>num</th>
                  <th>den</th>
                  <th>Type</th>
                  <th>Loop</th>
                  <th>Controller</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(system,index) in system_list" :key="index">
                   <td>{{ index+1  }}</td>
                   <td>{{ system.name  }}</td>
                   <td><input type="color" class="form-control form-control-sm btn-color" id="favcolor" name="favcolor" :value=system.color disabled></td>
                   <td>[{{ system.sys_num }}]</td>
                   <td>[{{ system.sys_den }}]</td>
                   <td>{{ system.sys_type }}</td>
                   <td>
                        <div v-if="system.controller_Cl">
                            <div class="badge badge-success">Closed</div>
                        </div>
                        <div v-else>
                            <div class="badge badge-danger">Open</div>
                        </div>
                    </td>
                    <td>
                        <div v-if="system.controller_type == 'none'">None</div>
                        <div v-if="system.controller_type == 'P'">Ki = {{system.controller_Ki}}</div>
                        <div v-if="system.controller_type == 'PI'">Ki = {{system.controller_Ki}}, Ti = {{system.controller_Ti}}</div>

                    </td>
                  <td><button @click="deleteSystem(index)" class="btn btn-sm btn_simple"><font-awesome-icon icon="trash" /></button></td>
                </tr>
               </tbody>
            </table>

            </div>
        </div>
    </div>
</div>
</template>

<script>
import { mapFields } from 'vuex-map-fields';

export default {
    name: 'ControllerApp',
    data() {
        return {
            server_error : null,
            name : null,
            color : null,
            sys_type : null,
            sys_num : null,
            sys_den : null,
            sys_Ts : null,
            controller_Cl : null,
            controller_type : null,
            controller_Ki : null,
            controller_Ti : null,
            Ts_disabled : null,
            Ki_disabled : null,
            Ti_disabled : null
        }
    },
    created : function () {
        this.init_selected_sys();
    },
    computed: {
        ...mapFields(['system_list','selected']),
        show_loop() {
            var value;
            if (this.controller_Cl==false)
                {
                value = "closed";
                }
            else
                {
                value = "open";
                }
            return value;
        }
    },
    methods: {
        init_selected_sys()
        {
        if (this.selected >= 0)
            {
            var selected_system =  this.system_list[this.selected];
            for(var k in selected_system)
                {
                this[k]=selected_system[k];
                }
            }
            this.change_system_type();
            this.change_controller_type();
        },
        change_system_type(){
            var values = {"continuous":1,"discrete":0};
            this.Ts_disabled = values[this.sys_type];
        },
        change_controller_type(){
            var values = {"none":[1,1],"P":[0,1],"PI":[0,0]};
            this.Ki_disabled = values[this.controller_type][0];
            this.Ti_disabled = values[this.controller_type][1];
            },
        deleteSystem(index)
        {
            this.system_list.splice(index,1);
            this.selected = this.system_list.length -1;
            this.init_selected_sys();
        },
        submit()
        {
        var data = {
                name : this.name,
                controller_Cl: this.controller_Cl,
                controller_Ki : this.controller_Ki,
                controller_Ti: this.controller_Ti,
                controller_type: this.controller_type,
                sys_num : this.sys_num,
                sys_den : this.sys_den,
                sys_Ts:   this.sys_Ts,
                sys_type: this.sys_type,
                color: this.color
                };

        this.$store.commit('add_system',data);
        this.$store.commit('change_selected',-1);
        }
    }
}

</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #2c3e50;
}

.badge{
    width: 60px;
}
</style>

