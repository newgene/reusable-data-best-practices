<template>
  <li class="node-tree" :class="[`toctree-l${node.level + 1} ${node.current?'current':''}`]">
    <div class="item-container">
      <button v-if="shouldBeCollapsible && node.children && node.children.length" v-on:click="toggleOpen" class="expand-button" 
      :style="{left: `${15 * (node.level + 1)}px`}">
        <span v-if="isOpen"> - </span>
        <span v-else> + </span>
      </button>
      <a :href="pathto(node.name?node.name:node.href)" class="reference internal" v-bind:class="{current: node.current}"
      v-bind:style="{paddingLeft: `${node.level==0?'':`${40 * node.level}px !important`}`}">{{ node.title }}</a>
    </div>
    <ul v-if="node.children && node.children.length" :style="{display: isOpen?'block': 'none'}">
      <node v-for="child in node.children" :nodeData="child" :key="child.title" ref="node"></node>
    </ul>
  </li>
</template>

<script>
export default {
  name: "node",
  props: {
    nodeData: Object
  },
  data: function (){
    let custom_toctree_values = JSON.parse(sessionStorage.getItem('custom_toctree_values'));

    return {
      isOpen: this.nodeData.level==1?false:true,
      shouldBeCollapsible: custom_toctree_values.collapsible,
      node: {}
    }
  },
  created() {

    // children in nodeData are given in linear format which does not help when making each section collapsible
    // This algorithm iterates each node and nests the nodes appropriately

    // First copy all necessary variables in their own variables to prevent mutating the nodeData prop
    let newNode = {...this.nodeData};
    let nodeDataChildren = [...this.nodeData.children];
    newNode.children = [];

    // this temporarely holds the fixed values
    let nestedNode = [];

    // here we iterate each child
    // children are in the format [{title: 'title1', level: 1}, {title: 'title2', level: 2}, {title: 'title3', level: 2}]
    // we have to nest the "level 2's" inside the "level 1's"
    nodeDataChildren.forEach(child=>{

      // if nestedNode is empty that means that the next item is an item that needs to be nested
      if(nestedNode.length > 0){

        // if child.level > nestedNode[0].level that means that the child needs to be nested in the 
        // nestedNode[0] top level section
        if(child.level > nestedNode[0].level){
          nestedNode[0].children.push(child);
        
        // else we should add the nestedNode[0] item in the newNode.children and then reset the nestedNode
        // then continue nesting the next top level section
        }else{
          newNode.children.push(nestedNode[0]);
          nestedNode.length = 0;
          child.children = [];
          nestedNode.push(child);
        }
      // if nestedNode is not empty that means that the next item is a top level section
      // so we assign a children prop in the current item and push it to the nestedNode value
      }else{
        child.children = [];
        nestedNode.push(child);
      }
    })

    this.node = newNode;
  },
  
  methods: {
    toggleOpen() {
      this.isOpen = !this.isOpen
    },
    expandAll: function(){
      this.isOpen = true;
      if(this.$refs.node){
        this.$refs.node.forEach(c => c.expandAll())
      }
    },
    collapseAll: function(){
      this.isOpen = false;
      if(this.$refs.node){
        this.$refs.node.forEach(c => c.collapseAll())
      }
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
};
</script>

<style scoped>
.item-container{
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.expand-button{
  position: absolute;
  transform: translateX(-50%);
  height: 15px;
  width: 15px;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #53a4b8;
  color: #5daabc;
  background-color: transparent;
  outline: none;
  top: 5px;
}
</style>