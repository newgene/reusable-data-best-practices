<template>
  <div class="header">
    <a :href="pathto('index')" class="header-item">Home</a>      
    <div style="flex:1;"></div>
    <a :href="pathto('about')" class="header-item">About</a>
  </div>
</template>

<script>
export default {
  name: 'Header',
  methods: {
    pathto (to){
      let mode = window.location.pathname.includes('_build') ? 'development' : 'production';
      let pathname = window.location.pathname;
      if(to.includes('#')){
        return to;
      }
      if(mode == 'development'){
        let index = pathname.substring(0, pathname.indexOf("html"));
        return index + 'html/' + `${to}.html`;
      }else{
        let index = pathname.location.pathname.substring(0,  pathname.location.pathname.indexOf("/", 4));
        return index + '/' + `${to}.html`;
      }
    },
  }
}
</script>

<style scoped>
.header{
  height: 60px;
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: center;
}

.header-item{
  /*padding: 0px 20px;*/
  cursor: pointer;
  text-decoration: none;
  color: black !important;
}
</style>