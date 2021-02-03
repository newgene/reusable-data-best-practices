<template>
  <ul v-bind:class="{ current: data.current }">
    <li v-for="entry in data.entries" :key="entry.name" class="toctree-l1" v-bind:class="{current: entry.current}">
      <a :href="pathto(entry.name)" class="reference internal" v-bind:class="{current: entry.current}">{{ entry.title }}</a>
    </li>
    {{ this.$children }}
  </ul>
</template>

<script>
export default {
  props: ['toc'],
  data: function (){
    return {
      data: this.toc,
    }
  },
  methods: {
    // can't access sphinx's pathto function so we have to compromise with our own
    pathto (to){
      let pathname = window.location.pathname;
      if(to.includes('#')){
        return to;
      }
      if(pathname.includes('chapters')){
        let index = pathname.substring(0,  pathname.indexOf("chapters"));
        return index + `${to}.html`;
      }

      if(pathname.includes('index.html')){
        let index = pathname.substring(0,  pathname.indexOf("index.html"));
        return index + `${to}.html`;
      }

      if(pathname.includes('search.html')){
        let index = pathname.substring(0,  pathname.indexOf("search.html"));
        return index + `${to}.html`;
      }
      return pathname + `${to}.html`;
    },
  },
}
</script>