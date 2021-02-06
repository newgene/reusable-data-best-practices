<template>
  <div>
    <div class="sidebar-group" id="toctree">
      <p class="caption">
        <span class="caption-text"><a :href="pathto('index')">Reusable data best practices</a></span>
      </p>
      <div style="margin:16px;">
          <div id="search-container" ></div>
      </div>
        <div class="flex" style="flex-direction: column;">
          <p class="sidebar-header">Contribute</p>
          <a class="sidebar-button" href="https://github.com/newgene/reusable-data-best-practices/">
              Contribute to our github page
          </a>
      </div>
      <p class="sidebar-header">Chapters</p>
      <toc-content-tree :treeData="toc"/>
      <!--<ul v-bind:class="{ current: toc.current }">
        <li v-for="entry in toc.children" :key="entry.name" class="toctree-l1" v-bind:class="{current: entry.current}">
          <a :href="pathto(entry.name)" class="reference internal" v-bind:class="{current: entry.current}">{{ entry.title }}</a>
          <ul v-if="entry.children">
            <li v-for="entry2 in entry.children" :key="entry2.name" class="toctree-l2" >
              <a :href="pathto(entry2.href)" class="reference internal"
              v-bind:style="{paddingLeft: `${30 * entry2.level}px !important`}">{{ entry2.title }}</a>
            </li>
          </ul>
        </li>
      </ul>-->
    </div>
  </div>
</template>

<script>
import TocContentTree from './TocContentTree.vue';

export default {
  components: {
    TocContentTree
  },
  data: function (){
    let toctree_data = JSON.parse(sessionStorage.getItem('toctree_data_json'))
    
    // original toctree_data is using mixed keys for the children values
    // specifically its using both "entries" and "children" as keys but we need to
    // choose one, so we create another object with the "entries" key removed
    // and replaced by "children"
    let toc = {
      children: toctree_data[0].entries,
      ...toctree_data[0]
    }

    delete toc.entries;
    return {
      //toc: toctree_data[0],
      toc: toc,
    }
  },
  methods: {
    // can't access sphinx's pathto function so we have to compromise with our own
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
        let index = pathname.substring(0,  pathname.indexOf("/", 4));
        return index + '/' + `${to}.html`;
      }
    },
  },
}
</script>

<style scoped>

</style>
