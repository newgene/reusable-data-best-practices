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
      <div class="collapse-buttons-container">
        <p class="sidebar-header">Chapters</p>
        <div class="collapse-buttons-container">
          <div v-on:click="expandAll" class="collapse-button" role="button">
            <span>Expand all</span>
            <svg xmlns="http://www.w3.org/2000/svg" style="transform: rotate(90deg);" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px" width="512.828px" height="512.828px" viewBox="0 0 512.828 512.828" xml:space="preserve">
            <g>
              <g>
                <g>
                  <path d="M33.105,473.415L0,428.339l234.096-171.928L0,84.49l33.104-45.077l264.785,194.459     c7.174,5.269,11.411,13.638,11.411,22.539c0,8.9-4.237,17.27-11.411,22.538L33.105,473.415z"/>
                </g>
                <g>
                  <path d="M236.635,473.415l-33.105-45.076l234.094-171.928L203.53,84.49l33.104-45.077l264.783,194.459     c7.174,5.268,11.411,13.637,11.411,22.538c0,8.899-4.237,17.271-11.411,22.538L236.635,473.415z"/>
                </g>
              </g>
            </g>
            </svg>
          </div>
          <div v-on:click="collapseAll" class="collapse-button" role="button">
            <span>Collapse all</span>
            <svg xmlns="http://www.w3.org/2000/svg" style="transform: rotate(270deg);" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px" width="512.828px" height="512.828px" viewBox="0 0 512.828 512.828" xml:space="preserve">
            <g>
              <g>
                <g>
                  <path d="M33.105,473.415L0,428.339l234.096-171.928L0,84.49l33.104-45.077l264.785,194.459     c7.174,5.269,11.411,13.638,11.411,22.539c0,8.9-4.237,17.27-11.411,22.538L33.105,473.415z"/>
                </g>
                <g>
                  <path d="M236.635,473.415l-33.105-45.076l234.094-171.928L203.53,84.49l33.104-45.077l264.783,194.459     c7.174,5.268,11.411,13.637,11.411,22.538c0,8.899-4.237,17.271-11.411,22.538L236.635,473.415z"/>
                </g>
              </g>
            </g>
            </svg>
          </div>
        </div>
      </div>
      <toc-content-tree :treeData="toc" ref="toctree"/>
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
  // created() {
  //   window.addEventListener('scroll', this.handleScroll);
  // },
  // unmounted () {
  //   window.removeEventListener('scroll', this.handleScroll);
  // },
  methods: {
    handleScroll () {
      const hash = window.location.hash;
      console.log(hash);

      let sections = document.getElementsByClassName('section');
      let referenceInternalLinks = document.getElementsByClassName('reference internal');

      sections.forEach(section=>{
        // let rect = section.getBoundingClientRect();
        if(section.offsetTop < window.pageYOffset && section.offsetTop + section.clientHeight){
          // if(history.pushState) {
          //   history.pushState(null, null, `#${section.id}`);
          // }
          // else {
          //   location.hash = `#${section.id}`;
          // }
          referenceInternalLinks.forEach(link=>{
            if(section.id==link.getAttribute("href").substring(1)){
              link.classList.add('current')
            }else{
              link.classList.remove('current');
            }
          })
        }
      })
      // referenceInternalLinks.forEach(link=>{
      //   console.log(link, hash)
      // })
    },
    expandAll: function(){
      this.$refs.toctree.expandAll();
    },
    collapseAll: function(){
      this.$refs.toctree.collapseAll();
    },
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
.collapse-buttons-container{
  display: flex;
  flex-flow: row wrap;
}
.collapse-button{
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #455458;
  padding: 5px;
  font-size: 1.2rem;
  margin: 3px;
  color: white;
  border-radius: 4px;
}

.collapse-button svg{
  width: 8px;
  height: 8px;
  margin-left: 5px;
  fill: white;
}
</style>
