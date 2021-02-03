<template>
  <div class="tree">
    <ul class="tree-list">
      <toc-node-tree :node="treeData"></toc-node-tree>
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
  }
};
</script>

<style>
.tree-list ul {
  padding-left: 16px;
  margin: 6px 0;
}
</style>