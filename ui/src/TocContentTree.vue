<template>
  <div>
    <ul v-bind:class="{ current: child.current }" v-for="child in treeData.children" :node="child" :key="child.title"
    style="margin: 0px;">
      <toc-node-tree :nodeData="child" ref="node"></toc-node-tree>
    </ul>
  </div>
</template>

<script>
import TocNodeTree from "./TocNodeTree";

export default {
  props: {
    treeData: Object
  },
  components: {
    TocNodeTree
  },
  data: function (){
    return{
      collapsed: null,
      expanded: null,
    }
  },
  methods: {
    expandAll: function(){
      this.$refs.node.forEach(c => c.expandAll())
    },
    collapseAll: function(){
      this.$refs.node.forEach(c => c.collapseAll())
    }
  }
};
</script>

<style>
.tree-list ul {
  padding-left: 16px;
  margin: 6px 0;
}
</style>
