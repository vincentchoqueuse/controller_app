<template>
  <div id="app" class="h-100">
    <nav class="navbar navbar-expand-lg navbar-white">
        <span class="navbar-brand"><font-awesome-icon icon="poll" size="1x"/></span>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>Controller App
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <router-link class="nav-link" to="/system">System</router-link>
                </li>   
                <li class="nav-item ">                 
                    <router-link class="nav-link" to="/step">Step Response</router-link>
                </li>
                <li class="nav-item ">
                    <router-link class="nav-link" to="/bode">Bode Plot</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/nichols">Nichols Chart</router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/zpmap">Poles / Zeros </router-link>
                </li>
            </ul>
        </div>
        <div class="form-inline my-2 my-lg-0">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a href="https://github.com/vincentchoqueuse/controller_app" class="nav-link" >Github</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="container-fluid h-100">
        <router-view />
    </div>
  </div>
</template>

<script>

export default {
    name: 'ControllerApp'
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}



.menu{
padding-bottom: 10px;
}


.left_sidebar{
border-right: #ced4da solid 1px;
}



</style>
